"""
This file contains scripts for running ADF calculations from python.  This depends on the ADF
python environment and therefore should not be imported normally as the required modules will
be missing.
"""
import copy
import logging
import pathlib
from typing import Mapping, Collection, Optional, Dict, List
import uuid

import ase
from ase import constraints
from ase import optimize
import mincepy
from pyos import psh

from dragonfruit import ase_utils
from . import constants

# pylint: disable=no-member

__all__ = "AdfTask", "AdfOptimisation"

logger = logging.getLogger(__name__)

DEFAULT_KEEP_EXTENSIONS = ("run", "xyz", "run", "out", "err", "logfile")


class AdfTask(mincepy.SimpleSavable, ase_utils.AseVisualizable):
    """A generic ADF task.  This can be used to store information about an ADF execution including
    the initial, final, and any intermediate structures (in the case of geometry optimisations).

    Typically this task would be subclassed to perform the particular workflow desired.
    """

    TYPE_ID = uuid.UUID("a9361ffe-708a-4cb6-b544-07e76e7a1d6a")

    atoms_history = mincepy.field("_atoms_history")
    take_charge_from = mincepy.field("take_charge_from", default=None)

    def __init__(
        self,
        initial_atoms: ase.Atoms,
        settings: Mapping,
        label: str = "",
        take_charge_from: str = None,
    ):
        """
        :param initial_atoms: the initial structure
        :param settings: the settings dictionary to pass to adfprepare
        :param label: the label for this (or these) ADF calculations
        :param take_charge_from: check the initial atoms metadata for the presence of
            a 'presumed_charge' field which, if there, will be used as the charge the the
            system.  Otherwise in the settings dictionary will be used (default being 0).
        """
        super().__init__()

        self._atoms = initial_atoms
        self._label = label or str(initial_atoms.get_chemical_formula())
        self._settings = copy.deepcopy(settings)  # The settings used for this run

        self._atoms_history = []
        self._atoms_history.append(mincepy.deepcopy(initial_atoms))

        self.take_charge_from = take_charge_from

    @mincepy.field("_atoms", ref=True)
    def atoms(self) -> ase.Atoms:
        """Get the current atoms, this is typically the update-to-date atoms, while the
        atoms_history holds copies of the atoms objects as the task progressed."""
        return self._atoms

    @mincepy.field("_label")
    def label(self) -> str:
        """Get the label for this task"""
        return self._label

    @mincepy.field("_settings")
    def settings(self) -> Mapping:
        """Get the settings that were used for this run"""
        return self._settings

    @property
    def initial_atoms(self) -> Optional[ase.Atoms]:
        if not self._atoms_history:
            return None

        return self._atoms_history[0]

    @property
    def final_atoms(self) -> Optional[ase.Atoms]:
        if not self._atoms_history:
            return None

        return self._atoms_history[-1]

    def get_visualizable(self):
        return self._atoms_history

    def load_instance_state(self, saved_state, loader: "mincepy.Loader"):
        super().load_instance_state(saved_state, loader)
        if self._atoms is None and self._atoms_history:
            self._atoms = mincepy.deepcopy(self.final_atoms)

    def _get_atoms_charge(self) -> Optional[float]:
        # Deal with atomic charges
        if self.take_charge_from == constants.ATOMS_META:
            # Try getting the charge from the metadata of the atoms
            atoms_meta = psh.meta(self.atoms)
            if atoms_meta and constants.META_PRESUMED_CHARGE in atoms_meta:
                return atoms_meta[constants.META_PRESUMED_CHARGE]
        elif self.take_charge_from:
            raise ValueError(
                "Unknown value for take_charge_from '{}'".format(self.take_charge_from)
            )

        return None


class AdfOptimisation(AdfTask):
    """An ADF geometry optimisation using ASE.

    This uses ASE to perform geometry optimisation calling the ADF code for energy/force
    evaluations.
    """

    TYPE_ID = uuid.UUID("86124647-c193-4d40-aefa-3ce34c42a7d4")

    keep_files = mincepy.field("keep_files")
    _files = mincepy.field("_files")

    def __init__(
        self,
        initial_atoms: ase.Atoms,
        settings: Mapping,
        label="",
        take_charge_from=constants.ATOMS_META,
        keep_extensions: Collection[str] = DEFAULT_KEEP_EXTENSIONS,
    ):
        """

        :param initial_atoms:
        :param settings:
        :param label:
        :param keep_extensions: the extensions of filenames to store in the task e.g.
            ['run', 'xyz'] etc.  The filenames are determined by the label.
            Note: the dot, '.', should be omitted.
        """
        super().__init__(initial_atoms, settings, label=label, take_charge_from=take_charge_from)
        self._results_history = []

        self.keep_files = list(self._label + "." + extension for extension in keep_extensions)
        self._files = ()

    @property
    def stored_files(self) -> Dict[str, mincepy.builtins.BaseFile]:
        """The dictionary of stored files.
        These are updated each time the run is saved based on the keep files attribute"""
        return {file.filename: file for file in self._files}

    @mincepy.field("_results_history")
    def results_history(self) -> List:
        return self._results_history

    def run(self, fmax=0.05, max_steps=1000, **kwargs):
        """Run the optimisation for until the maximum force threshold or the maximum number
        of steps is reached."""

        # Import here so that this file doesn't fail to import if the user doesn't have ADF
        from ase.calculators import (
            scm,
        )  # pylint: disable=import-outside-toplevel, no-name-in-module

        # For legacy reasons, check if steps has been supplied
        max_steps = kwargs.get("steps", max_steps)

        system = self.atoms
        settings = self.settings.copy()

        # Deal with atomic charges
        try:
            charge = self._get_atoms_charge()
            if charge is not None:
                settings[constants.ADFPREP_CHARGE] = charge
        except ValueError as exc:
            logger.warning(str(exc))

        prep_options = create_prep_str(settings, t=self.label)

        print(f"Running {system} with '{prep_options}'")
        try:
            calculator = scm.ADFCalculator(label=self.label, adfprep_options=prep_options)
        except TypeError:
            # The syntax is this in the 2020 version
            calculator = scm.ADFCalculator(label=self.label, amsprep_options=prep_options)

        # Constrain the CoM
        system.set_constraint(constraints.FixCom())
        system.set_calculator(calculator)  # pylint: disable=no-member
        optimiser = optimize.BFGS(system)

        # Set up the observer
        run_path = pathlib.Path(self.label)

        def stepped():
            """Called after the optimiser makes a step"""
            self._results_history.append(dict(calculator.results))

            # The first call to the observer is the calculation that corresponds to the initial
            # atoms which we already have in our history, so skip it
            if optimiser.nsteps != 0:
                self.atoms_history.append(mincepy.deepcopy(optimiser.atoms))

            self._update_files(run_path)
            self.save()

        optimiser.attach(stepped, interval=1)

        optimiser.run(fmax=fmax, steps=max_steps)

        return system

    def _update_files(self, run_path: pathlib.Path):
        """Update the stored files from those currently on disk in the run path.

        Note: This does not update the atoms history.  That's left up to the caller"""
        current_files = self.stored_files
        found_files = []
        for filename in self.keep_files:
            abspath = pathlib.Path(run_path) / filename
            if abspath.exists():
                try:
                    file = current_files[filename]
                except KeyError:
                    # New file
                    file = mincepy.get_historian().create_file(filename=filename)
                file.from_disk(abspath)
                found_files.append(file)

        self._files = tuple(found_files)


def optimise(system: ase.Atoms, settings: Mapping, fmax=0.01, max_steps=1000):
    opt = AdfOptimisation(system, settings)
    opt.run(fmax, max_steps)
    return opt


def create_prep_str(settings: Mapping, **overrides) -> str:
    """Given a settings dictionary return the adfprep string"""
    settings = dict(settings)
    settings.update(overrides)

    return " ".join([f"-{key} {value}" for key, value in settings.items()])


MINCEPY_TYPES = AdfTask, AdfOptimisation
