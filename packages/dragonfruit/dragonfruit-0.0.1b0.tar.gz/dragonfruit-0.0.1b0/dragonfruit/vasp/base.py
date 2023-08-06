from copy import deepcopy
import logging
import os
from pathlib import Path
import shutil
import typing
from typing import Optional, Dict
import uuid

import ase
from ase.io import read as ase_read
from ase.io import ParseError as AseParseError
from ase.calculators import vasp
import ase.calculators.calculator

import mincepy
import dragonfruit as df
from dragonfruit import mince, utils
from . import vasp_errors
from . import vasp_parsers as vp

__all__ = "VaspRun", "VaspTask", "CRASHED", "CONVERGED"

_LOGGER = logging.getLogger(__name__)

DEFAULT_KEEP_FILES = (
    "POSCAR",
    "INCAR",
    "KPOINTS",
    "IBZKPT",
    "vasprun.xml",
    "OUTCAR",
    "CONTCAR",
    "OSZICAR",
    "ase-sort.dat",
)

CRASHED = "crashed"
CONVERGED = "converged"


class VaspRun(mince.Process, df.AseVisualizable):
    # pylint: disable=too-many-public-methods,too-many-instance-attributes
    TYPE_ID = uuid.UUID("139d0f75-7178-43fe-85e4-f609469122e1")
    # List of things to save.  Remember to update if adding any new attributes
    ATTRS = (
        mincepy.AsRef("initial_atoms"),
        "_atom_steps",
        "_result_steps",
        "_settings",
        "_sort",
        "_resort",
        "_run_path",
        "_vasp_stdout",
        "_scheduler_env",
        "description",
        "_files",
        "keep_files",
        "_files",
        "_settings_overwrites",
        "post_calculation_state",
    )

    def __init__(
        self,
        atoms: ase.Atoms,
        settings: dict,
        run_path: Path = None,
        description="",
        keep_files=DEFAULT_KEEP_FILES,
    ):
        """Takes the atoms, vasp calculator settings and optionally directory on where to run

        :param atoms: the atoms to run on
        :param settings: the VASP calculator settings dictionary
        :param run_path: the path that VASP runs in
        :param description: an optional description of this run
        :param keep_files: the files to keep each time this run is saved
        """

        super().__init__("vasp-run")
        self.initial_atoms = atoms  # These should be kept immutable and not be changed

        # Snapshots of atomic geometry from this run
        # contains tuples of Atoms and a result dictionary (Atoms, result dictionary)
        self._atom_steps = mincepy.builtins.RefList()  # type: typing.MutableSequence[ase.Atoms]
        self._result_steps = []  # type: typing.MutableSequence[dict]

        # The VASP settings as passed to the calculator
        self._settings = settings
        # Settings used to update this run's settings but are not propagated to restarts
        self._settings_overwrites = {}

        self.description = description

        # A dictionary of results from the run
        self._sort, self._resort = utils.get_atoms_sort_map(atoms)

        # Keywords we need to figure out how to update
        self._run_path = (run_path or Path(".")).resolve()
        self._vasp_stdout = None

        # Try to get information about the scheduler we're running with (if any)
        self._scheduler_env = df.get_scheduler_environment()

        self._files = ()
        self.keep_files = list(keep_files)

        # Information about the job, to be filled in during "update_results"
        self.post_calculation_state = None

    def __str__(self):
        return "{} [{} steps, (done: {}, converged: {})]".format(
            self.description, len(self._atom_steps), self.done, self.converged
        )

    @classmethod
    def from_vasp_run(cls, run_directory: Path):
        # Instantiate a vasp run from an existing vasp directory
        atoms = ase_read(run_directory / "POSCAR")
        settings = vasp.Vasp(restart=True, directory=run_directory).todict()
        run = VaspRun(atoms, settings, run_directory)
        run.update_results()
        return run

    @property
    def vasp_stdout(self):
        return self._vasp_stdout

    @vasp_stdout.setter
    def vasp_stdout(self, value):
        if value is None:
            self._vasp_stdout = None
            return

        if not isinstance(value, str):
            raise TypeError("Must pass a string")

        if value == "-":
            raise ValueError("Cannot pass file stream")

        if self._vasp_stdout in self.keep_files:
            self.keep_files.remove(self._vasp_stdout)

        self._vasp_stdout = value
        if value not in self.keep_files:
            self.keep_files.append(value)

    @property
    def sort(self) -> typing.List:
        return self._sort

    @property
    def resort(self) -> typing.List:
        return self._resort

    @property
    def atoms_history(self) -> typing.Sequence[ase.Atoms]:
        """Get a list of all the atoms from this run"""
        return self._atom_steps

    @property
    def results_history(self) -> typing.Sequence[dict]:
        """Get a list of all the results dictionaries for this run"""
        return self._result_steps

    @property
    def run_path(self) -> Path:
        """The folder where this VASP calculation runs"""
        return self._run_path

    @property
    def settings(self) -> typing.Dict:
        """The vasp calculator settings"""
        return self._settings

    @property
    def settings_overwrites(self) -> typing.Dict:
        """A dictionary that can be used to overwrite particular keys for this run without
        propagating them to any restarts of this run"""
        return self._settings_overwrites

    def _convert_special_keywords(self, settings: typing.Dict) -> typing.Dict:
        """Grab some special keywords from settings, and make approprivate adjustments
        Returns the adjusted settings dictionary"""
        if "kptdensity" in settings:
            atoms = self.initial_atoms
            kptdensity = settings.pop("kptdensity")
            kpts = ase.calculators.calculator.kptdensity2monkhorstpack(
                atoms, kptdensity=kptdensity, even=False
            )
            settings["kpts"] = kpts
        return settings

    @property
    def run_settings(self) -> typing.Dict:
        """The _actual_ settings this will run with if calling run().  This returns a dictionary
        that is a copy of `self.settings.update(self.settings_overwrites)`."""
        settings = self.settings.copy()
        settings.update(self.settings_overwrites)
        settings = self._convert_special_keywords(settings)
        return settings

    @property
    def atoms(self) -> ase.Atoms:
        """Get the latest atoms"""
        if self._atom_steps:
            return self._atom_steps[-1]
        return self.initial_atoms

    @property
    def results(self) -> Optional[dict]:
        """Get the latest results, returns None if there aren't any yet"""
        if self._result_steps:
            return self._result_steps[-1]
        return None

    @property
    def scheduler_env(self) -> Optional[df.SchedulerEnvironment]:
        return self._scheduler_env

    @property
    def stored_files(self) -> Dict[str, mincepy.builtins.BaseFile]:
        """The dictionary of stored files.
        These are updated each time the run is saved based on the keep files attribute"""
        return {file.filename: file for file in self._files}

    def get_file_contents(self, filename, encoding="utf-8"):
        """Get the content of a stored file"""
        if encoding is None:
            args = {"mode": "rb"}
        else:
            args = {"mode": "r"}
        try:
            with self.stored_files[filename].open(**args) as stream:
                return stream.read()
        except KeyError:
            raise ValueError(
                "Unknown file '{}', try one of '{}'".format(filename, self.stored_files.keys())
            ) from None

    def print_file_contents(self, filename, encoding="utf-8"):
        """ "Prints the contents from .get_file_contents"""
        print(self.get_file_contents(filename, encoding))

    @mincepy.track
    def run(self):
        """Run VASP with the current settings, atoms in the running path.
        We don't run if we already did the calculation
        """
        if self.results is not None:
            return

        with self.running():
            calc = vasp.Vasp(**self.run_settings)
            try:
                self.vasp_stdout = calc.txt
            except (ValueError, TypeError):
                pass
            to_run = deepcopy(self.initial_atoms)
            to_run.calc = calc
            try:
                to_run.get_potential_energy()
            except ase.calculators.calculator.CalculationFailed as exc:
                _LOGGER.error("VASP calculation failed with exception: %s", exc)
            except ase.calculators.calculator.ReadError as exc:
                _LOGGER.error(
                    "VASP raised a read error, indicating corrupted output files: %s", exc
                )
            except Exception as exc:  # pylint: disable=broad-except
                # Check if we know that this is due to a read error from ASE
                if not vp.is_output_corrupt(path=self.run_path):
                    # Both output files were uncorrupted, something else must've happened
                    raise
                _LOGGER.error(
                    (
                        "An Error was found - this is likely due to a silent calculation"
                        " error by VASP. I am ignoring this error: %s"
                    ),
                    exc,
                )

            self.update_and_set_results()

    @mincepy.track
    def fake_run(self):
        """Run VASP with the current settings, atoms in the running path"""
        with self.running():
            calc = vasp.Vasp(**self.run_settings)
            try:
                self.vasp_stdout = calc.txt
            except (ValueError, TypeError):
                pass
            to_run = deepcopy(self.initial_atoms)
            to_run.calc = calc

            # pylint: disable=protected-access
            calc._run(calc.make_command())
            self.update_and_set_results()

    def update_and_set_results(self) -> None:
        """Update the results, and set as completed."""
        if self.done:
            _LOGGER.warning("Attempted to update results of completed VaspRun.")
            return
        update_success = self.update_results()
        _LOGGER.info("Updated results in VaspRun. Succes? %s", update_success)
        self.set_result(self.results)

    @mincepy.track
    def update_results(self) -> bool:
        """Returns true if it managed to update with new results.
        Will not update if we already have results present"""

        # We already did an update
        if self.post_calculation_state is not None:
            return False

        # Check if we have already done a read and inserted results
        if self.results is not None:
            return False

        outcar = self.run_path / "OUTCAR"
        if not outcar.exists():
            return False

        self.post_calculation_state = {}
        self.post_calculation_state[CRASHED] = vp.read_is_crashed(outcar)
        self.post_calculation_state[CONVERGED] = vp.read_is_converged(outcar)

        # Let's try and load the atoms, and see if we need to append them
        ok_files = vp.get_ok_output_files(path=self.run_path)
        if len(ok_files) == 0:
            # We cannot parse any output files
            return False

        if "OUTCAR" in ok_files:
            # Prefer the OUTCAR reader
            try:
                images = ase_read(self.run_path / "OUTCAR", index=":")
            except AseParseError:
                # Something might've happened during the calculation, which corrupted
                # some intermediate images.
                # Try just recovering the last image
                try:
                    images = [ase_read(self.run_path / "OUTCAR", index=-1)]
                except AseParseError:
                    # Reading last image also failed
                    return False
            # XXX: There is a bug in ASE 3.21.1, where the OUTCAR reader doesn't set the PBC
            # this is fixed in the master of ASE, so it will go away in 3.21.2
            for atoms in images:
                atoms.pbc = True
        else:
            # use the XML reader, greedy reader
            images = ase_read(self.run_path / "vasprun.xml", index=":")

        if not images:
            # Images is empty
            return False
        scf_energies = vp.parse_scf(outcar)
        ediff = self.run_settings.get("ediff", 1e-4)  # 1E-4 is the VASP default
        scf_converged = scf_energies <= ediff

        if len(scf_converged) > len(images) and len(images) == 1:
            # We might've only recovered the last image, so assume the last value in scf_converged
            # belongs to the image
            scf_converged = scf_converged[-1:]

        # Update all the images
        for scf_conv, image in zip(scf_converged, images):
            atoms, results = utils.resort_atoms_and_results(image, self.resort)
            atoms.info["scf_converged"] = bool(scf_conv)
            self._atom_steps.append(atoms)
            self._result_steps.append(results)

        return True

    @property
    def converged(self) -> bool:
        state = self.post_calculation_state
        if state is not None:
            return state.get(CONVERGED, False)
        return False

    @property
    def crashed(self) -> bool:
        state = self.post_calculation_state
        if state is not None:
            return state.get(CRASHED, False)
        return False

    @mincepy.track
    def create_restart(
        self,
        new_path: Path = None,
        atoms: ase.Atoms = None,
        copy_files=("WAVECAR",),
        init_kwargs: dict = None,
    ):
        """
        Create a restart from this VaspRun and give back a new VaspRun ready to be executed

        :param new_path: the new path to run the restart in
        :param atoms: Optionally specify a specific atoms object to use.
            Default: Use the last atoms in the task.
        :param copy_files: the files to copy over to the new path for the restart
        :param init_kwargs: will be passed on to the constructor of the new VaspRun
        """
        init_kwargs = init_kwargs or {}
        init_kwargs["run_path"] = new_path

        atoms = atoms or self.atoms

        restart = VaspRun(deepcopy(atoms), deepcopy(self.settings), **init_kwargs)

        prev_path = self.run_path.resolve()
        new_path = restart.run_path

        # If the new path is different from the old, exists and we can at least read it,
        # then copy the files
        if new_path != prev_path and prev_path.exists() and os.access(str(prev_path), os.R_OK):
            for file in copy_files:
                shutil.copyfile(prev_path / Path(file), new_path / Path(file))

        return restart

    @mincepy.track
    def save_instance_state(self, saver):
        stored_files = self.stored_files.copy()
        # Update the stored file
        to_remove = set(stored_files.keys())
        for filename in self.keep_files:
            try:
                with open(self._run_path / filename, "rb") as disk_stream:
                    try:
                        db_file = stored_files[filename]
                    except KeyError:
                        # New file
                        db_file = saver.get_historian().create_file(filename=filename)
                        stored_files[filename] = db_file

                    with db_file.open("wb") as db_stream:
                        shutil.copyfileobj(disk_stream, db_stream)

                to_remove.discard(filename)
            except FileNotFoundError:
                pass

        # Get rid of the remaining ones
        for filename in to_remove:
            stored_files.pop(filename, None)

        self._files = tuple(stored_files.values())

        # Call the super to save
        saved_state = super().save_instance_state(saver)

        # Update meta
        self.update_meta(dict(converged=self.converged, crashed=self.crashed))
        return saved_state

    def load_instance_state(self, saved_state, loader):
        self.description = ""
        super().load_instance_state(saved_state, loader)
        if "_settings_overwrites" not in vars(self):
            self._settings_overwrites = {}

    def get_visualizable(self):
        return self.atoms_history


class VaspTask(mince.Process, df.AseVisualizable):
    """Represents a particular VASP task like geometry optimisation or singlepoint calculation.
    This could involve multiple restarts until it is completed which is why it has a list of
    individual vasp executions called `VaspRun`s.
    """

    TYPE_ID = uuid.UUID("0420e8e1-1315-4d0c-b1b1-0f20f3686fa0")
    ATTRS = mincepy.AsRef("_initial_atoms"), "_initial_settings", "_runs", "_restarter"

    def __init__(self, initial_atoms: ase.Atoms, initial_settings: dict):
        super().__init__("vasp-task")
        with self.running():
            self._initial_atoms = initial_atoms
            self._initial_settings = initial_settings
            self._restarter = vasp_errors.RunRestarter()
            self._runs = mincepy.builtins.RefList()

    def __str__(self):
        desc = ["{} runs".format(len(self._runs))]
        if self._runs:
            desc.append(str(self._runs[-1]))
        return " ".join(desc)

    @property
    def runs(self) -> typing.Sequence[VaspRun]:
        return self._runs

    @property
    def initial_atoms(self) -> ase.Atoms:
        """Get the initial atoms object"""
        return self._initial_atoms

    @property
    def initial_settings(self) -> dict:
        return self._initial_settings

    @property
    def settings(self):
        """The current settings"""
        if self.runs:
            return self.runs[-1].settings
        return self._initial_settings

    @property
    def atoms(self):
        """The current atoms"""
        if self.runs:
            return self.runs[-1].atoms
        return self._initial_atoms

    @property
    def results(self) -> Optional[dict]:
        """Get the latest results, returns None if there aren't any yet"""
        if self.runs:
            return self.runs[-1].results
        return None

    @property
    def converged(self) -> bool:
        if self.runs:
            return self.runs[-1].converged
        return False

    @property
    def crashed(self) -> bool:
        if self.runs:
            return self.runs[-1].crashed
        return False  # Same logic as in the VaspRun

    def append_run(self, vasp_run: VaspRun):
        self._runs.append(vasp_run)

    def get_last_run(self) -> Optional[VaspRun]:
        if not self._runs:
            return None
        return self._runs[-1]

    def get_restarter(self) -> vasp_errors.RunRestarter:
        return self._restarter

    @mincepy.track
    def new_run(self, **kwargs) -> VaspRun:
        """
        Gives you a new run for this task.  If there are previous runs in this task the new run
        will be initialised with atoms and settings from the previous.
        Otherwise initial settings are used.

        The new run will be appended to our list of runs.
        THe previous run (if present) will have its state set to done if not already done so which
        means it can no longer be modified.
        """
        if self._runs:
            last_run = self._runs[-1]  # type: VaspRun
            new_run = VaspRun(deepcopy(last_run.atoms), deepcopy(last_run.settings), **kwargs)
        else:
            # We cannot run on atoms with vacancies
            # also, run on a copy, so we don't mutate the original initial
            initial_atoms = prepare_atoms(self.initial_atoms)
            new_run = VaspRun(initial_atoms, self.initial_settings, **kwargs)
        self._runs.append(new_run)
        return new_run

    @property
    def atoms_history(self) -> typing.List[ase.Atoms]:
        """Get a list of all the atoms from this task (spanning all runs)"""
        return [atoms for run in self.runs for atoms in run.atoms_history]

    @property
    def results_history(self):
        """Get a list of all the results dictionaries for this task (spanning all runs)"""
        return [atoms for run in self.runs for atoms in run.results_history]

    def save_instance_state(self, saver) -> dict:
        state = super().save_instance_state(saver)
        self.update_meta(dict(converged=self.converged))
        return state

    def execute_run(self, vasp_run: VaspRun):
        if vasp_run not in self.runs:
            # Should we require this, i.e. assert?
            self.runs.append(vasp_run)
        df.save(self)
        _LOGGER.info("Executing:\nSettings: %s\nAtoms: %s", vasp_run.settings, vasp_run.atoms)
        with vasp_run.running():
            vasp_run.run()
        df.save(vasp_run)

    def get_visualizable(self):
        return self.atoms_history


def filter_atoms(atoms: ase.Atoms) -> None:
    """Pre-process an atoms object, removing vacancies"""
    idx = [atom.index for atom in atoms if atom.symbol == "X"]
    if idx:
        del atoms[idx]


def prepare_atoms(atoms: ase.Atoms) -> ase.Atoms:
    atoms = deepcopy(atoms)
    filter_atoms(atoms)
    return atoms


HISTORIAN_TYPES = VaspRun, VaspTask
