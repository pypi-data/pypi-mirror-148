"""Module containing scripts and workflows for running ADF through the PLAMS interface"""
import logging
import pathlib
import shutil
from typing import Union, Dict
import uuid

import ase
from ase.calculators import singlepoint
import mincepy
from scm import plams

from . import adf_scripts
from . import constants

# pylint: disable=no-member

__all__ = ("PlamsTask",)

logger = logging.getLogger(__name__)


class PlamsTask(adf_scripts.AdfTask):
    """An ADF task using the PLAMS interface which is more stable and complete than the ASE one.

    See https://www.scm.com/doc/plams/ for documentation.
    """

    TYPE_ID = uuid.UUID("31106151-53d4-446c-9a0c-fc856462ae1a")

    _files = mincepy.field("_files")

    def __init__(
        self,
        initial_atoms: ase.Atoms,
        settings: plams.Settings,
        label: str = "",
        take_charge_from=constants.ATOMS_META,
    ):
        super().__init__(initial_atoms, settings, label, take_charge_from=take_charge_from)
        self._files = list()

    def run(self):
        plams.init()
        job = self._create_ams_job()
        print("Running PLAMS job")
        results = job.run()

        # Now copy over the results into our atoms
        results_to_atoms(self.atoms, results)
        self.atoms_history.append(mincepy.deepcopy(self.atoms))

        # Now save any of the output files we want to keep
        self._update_files(job, results)

        self._run_density(job)

    @property
    def stored_files(self) -> Dict[str, mincepy.builtins.BaseFile]:
        """The dictionary of stored files.
        These are updated each time the run is saved based on the keep files attribute"""
        return {file.filename: file for file in self._files}

    def _update_files(self, job: plams.AMSJob, results: plams.AMSResults):
        """Update the stored files from those currently on disk in the run path.

        Note: This does not update the atoms history.  That's left up to the caller"""
        print(f"Saving selected PLAMS files from {job.path}")
        job_path = pathlib.Path(job.path)
        found_files = []
        for filename in results.files:
            abspath = job_path / filename
            file = self._update_file(abspath)
            if file is not None:
                found_files.append(file)

        self._files = list(found_files)

    def _update_file(self, abspath: pathlib.Path) -> mincepy.File:
        file = None
        filename = abspath.name
        if abspath.exists():
            try:
                file = self.stored_files[filename]
            except KeyError:
                # New file
                file = mincepy.get_historian().create_file(filename=filename)

            # Have to deal with binary files specially
            binary = False
            if abspath.suffix in (".rkf", ".rel", ".dill") or abspath.name.startswith("t21"):
                binary = True

            logger.debug("Saving file '%s' in task", abspath)
            if binary:
                with open(abspath, "rb") as inp, file.open(mode="wb") as out:
                    shutil.copyfileobj(inp, out)
            else:
                file.from_disk(abspath)

        return file

    def _run_density(self, job):
        dens_job = plams.DensfJob(
            pathlib.Path(job.path) / "adf.rkf",
            settings=create_densf_settings(grid="medium", cuboutput="density.cub"),
            name=f"{job.name}-densf",
        )

        print("Launching charge density grid calculation")
        dens_results = dens_job.run()
        if dens_job.check():
            print("Density job completed successfully")
        else:
            print("Density job completed unsuccessfully")

        # Now store all the cube files
        job_path = pathlib.Path(dens_job.path)
        for filename in dens_results.files:
            if filename.endswith(".cub"):
                abspath = job_path / filename
                if abspath.exists():
                    try:
                        file = self.stored_files[filename]
                    except KeyError:
                        # New file
                        file = mincepy.get_historian().create_file(filename=filename)
                        self._files.append(file)

                    with open(abspath, "rb") as inp, file.open(mode="wb") as out:
                        shutil.copyfileobj(inp, out)

    def _create_ams_job(self) -> plams.AMSJob:
        """Create the AMSJob for this task"""
        mol = plams.fromASE(self.atoms)
        # Deal with atomic charges
        try:
            charge = self._get_atoms_charge()
            if charge is not None:
                mol.properties.charge = charge
        except ValueError as exc:
            logger.warning(str(exc))

        return plams.AMSJob(molecule=mol, settings=self.settings, name=self.label)


def to_results_calculator_dict(results: plams.Results) -> dict:
    """Turn a PLAMS Results into a dictionary that can be passed to a calculator"""
    results_dict = {}
    try:
        results_dict["energy"] = results.get_energy(unit="eV")
    except KeyError:
        pass
    try:
        results_dict["forces"] = results.get_gradients(energy_unit="eV", dist_unit="A")
    except KeyError:
        pass
    return results_dict


def results_to_atoms(atoms: ase.Atoms, results: plams.Results):
    """Copy the results from the PLAMS calculation into the passed atoms object (including attached
    calculator)"""
    # Now copy over the results into our atoms
    final_atoms = plams.toASE(results.get_main_molecule())
    atoms.positions = final_atoms.positions
    atoms.numbers = final_atoms.numbers

    spoint = singlepoint.SinglePointCalculator(atoms, **to_results_calculator_dict(results))
    atoms.calc = spoint


def default_adf_settings() -> plams.Settings:
    """Create a default set of geometry optimisation settings"""
    settings = plams.Settings()
    settings.input.ADF.basis.type = "TZP"  # Triple zeta
    settings.input.ADF.basis.core = "None"  # Frozen-core
    settings.input.ADF.xc.hybrid = "B3LYP"
    settings.input.ADF.xc.dispersion = "Grimme3"
    settings.input.ADF.symmetry = "NOSYM"  # Turn off symmetry detection

    return settings


def create_densf_settings(grid: Union[str] = "fine", cuboutput: str = None) -> plams.Settings:
    """Helper function to create settings for a densf job

    See https://www.scm.com/doc/ADF/Input/Densf.html for full input block specification

    :param grid: can be either 'coarse', 'medium' or 'fine'
    """
    settings = plams.Settings()
    settings.input.density = "scf"
    if grid is not None:
        settings.input.grid._h = grid  # pylint: disable=protected-access

    if cuboutput is not None:
        settings.input.cuboutput = cuboutput

    return settings


def optimise(system: ase.Atoms, settings: plams.Settings) -> PlamsTask:
    settings = settings.copy()
    settings.input.AMS.Task = "GeometryOptimization"
    opt = PlamsTask(system, settings)
    opt.run()
    return opt


MINCEPY_TYPES = (PlamsTask,)
