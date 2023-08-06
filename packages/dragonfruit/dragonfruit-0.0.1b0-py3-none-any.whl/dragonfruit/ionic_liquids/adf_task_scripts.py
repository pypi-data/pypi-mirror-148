"""Scripts for creating ADF tasks that will be run with minkipy and pyos"""
import random
import string
from typing import Mapping, Optional

import ase
import ase.build.attach
import minkipy
from pyos import db
from pyos import pathlib
from pyos import psh
from pyos import os as pos
from scm import plams

from . import constants
from . import plams_scripts

__all__ = "optimise_pair_task", "optimise_task", "get_pair_name"

# pylint: disable=no-member

DEFAULT_RUN_FOLDER = pathlib.Path(".runs/")
ADF_SETTINGS = "adf_settings"  # The ADF settings dictionary name, used as a default for tasks
# The ADF settings dictionary name, used as a default for tasks
PLAMS_SETTINGS = "plams_adf_settings"


def random_string(length=5) -> str:
    letters = string.ascii_lowercase
    return "".join(random.sample(letters, length))


def get_name(system: ase.Atoms) -> str:
    """Get a name for a the atoms object"""
    path = db.get_path(system)
    if path is None:
        # Use the chemical formula
        return str(system.get_chemical_formula())

    return pathlib.Path(path).name


def get_pair_name(molecule1: ase.Atoms, molecule2: ase.Atoms) -> str:
    """Create a name for a pair of molecules"""

    name1 = get_name(molecule1)
    name2 = get_name(molecule2)

    # Always order by smaller molecule first
    if len(molecule1) < len(molecule2):
        return f"{name1}-{name2}"

    return f"{name2}-{name1}"


def _get_default_path(label: str) -> str:
    # Set the pyos path
    return pos.path.abspath(f"./.runs/{label}")


def _load_settings(settings_spec: Optional) -> Mapping:
    # Try loading using standard library
    settings = psh.load(settings_spec)
    if not isinstance(
        settings, Mapping
    ):  # pylint: disable=isinstance-second-argument-not-valid-type
        raise TypeError(
            "Settings were loaded but are not a mapping type, got '{}'".format(
                settings.__class__.__name__
            )
        )

    return settings


def _get_settings(settings_spec) -> plams.Settings:
    """Get the ADF settings, either as the passed dictionary, loaded from a path/obj id/etc or,
    if None, the default settings will try to be loaded from the current folder"""
    if settings_spec is None:
        # Try the default
        if pathlib.Path(PLAMS_SETTINGS).exists():
            settings = _load_settings(PLAMS_SETTINGS)
        else:
            # Just use the default, empty settings
            settings = plams.Settings()

    elif isinstance(
        settings_spec, Mapping
    ):  # pylint: disable=isinstance-second-argument-not-valid-type
        settings = _plams_settings(settings_spec)
    else:
        # All else failed, so maybe it's an object ID or path
        settings = _load_settings(settings_spec)

    return _plams_settings(settings)


def optimise_task(
    system, settings: Mapping = None, pyos_path=None, worker_task_folder=None
) -> minkipy.Task:
    """Create an optimisation task that can be submitted to a minki queue

    If not settings are supplied, the task will look for an object called 'adf_settings' in the
    current folder.  If it fails to find this, an empty dictionary will be used.

    The pyos_path defaults to './.runs/[system obj id]'
    and the worker_task_folder to './[system obj id]'

    :param worker_task_folder: the path (relative or absolute) on disk where the worker should
        run the task
    """
    # SYSTEM
    # Load the system, this way the user can pass paths, the object itself or an object id
    # and it will work
    if not isinstance(system, ase.Atom):
        system = psh.load(system)

    system_obj_id = psh.save(system)

    if worker_task_folder is None:
        worker_task_folder = f"./{system_obj_id}"

    # SETTINGS
    settings = _get_settings(settings)
    settings.input.AMS.Task = "GeometryOptimization"  # Turn on geometry optimisation

    # TASK
    plams_task = plams_scripts.PlamsTask(system, settings)
    task = minkipy.task(plams_task.run, dynamic=True, folder=worker_task_folder)

    # Set the pyos path
    if pyos_path is None:
        pyos_path = (DEFAULT_RUN_FOLDER / get_name(system)).to_dir().resolve()
    task.pyos_path = pyos_path

    with pathlib.working_path(pyos_path):
        # Save everything path related in the pyos_path
        psh.save(task)

    return task


def _get_presumed_charge(*atoms_obj):
    """Get the presumed charge(s) for the passed objects from their metadata"""
    charges = []
    for entry in atoms_obj:
        meta = psh.meta(entry)
        if meta:
            if constants.META_PRESUMED_CHARGE in meta:
                charges.append(meta[constants.META_PRESUMED_CHARGE])
            else:
                charges.append(None)
        else:
            charges.append(None)

    if len(atoms_obj) == 1:
        return charges[0]

    return tuple(charges)


def optimise_pair_task(
    molecule1,
    molecule2,
    distance: float = 1,
    settings=None,
    pyos_folder="./",
    worker_task_folder=None,
) -> minkipy.Task:
    """Given a pair of molecules create a new system containing the two separated by some distance
    but otherwise randomly placed and return the geometry optimisation task that can be submitted
    """
    if not isinstance(molecule1, ase.Atoms):
        molecule1 = psh.load(molecule1)
    if not isinstance(molecule2, ase.Atoms):
        molecule2 = psh.load(molecule2)

    # Make sure both molecule 1 and 2 are saved so we can use their object ids
    psh.save(molecule1, molecule2)

    # Create a new molecule
    joined = ase.build.attach.attach_randomly(molecule1, molecule2, distance)
    pair_name = get_pair_name(molecule1, molecule2)
    # Create a base directory where this molecule pair will live
    basedir = pathlib.Path(pyos_folder) / pair_name

    # Give the molecule a name consisting of the pair plus a short random string
    molecule_name = pair_name + f"-{random_string(5)}"
    psh.save(joined, basedir / molecule_name)

    oids = list(psh.oid(molecule1, molecule2))
    # Now update the metadata on the joined molecule so we know where it came from
    joined_meta = {constants.META_PARENT_MOLECULES: oids}

    # Set the correct presumed charge
    charge1, charge2 = _get_presumed_charge(molecule1, molecule2)
    if charge1 is not None or charge2 is not None:
        if charge1 is None:
            joined_charge = charge2
        elif charge2 is None:
            joined_charge = charge1
        else:
            joined_charge = charge1 + charge2

        joined_meta[constants.META_PRESUMED_CHARGE] = joined_charge

    psh.meta - psh.u(joined, **joined_meta)  # pylint: disable=expression-not-assigned

    # Create a path for the optimisation task
    optimise_folder = (basedir / DEFAULT_RUN_FOLDER / molecule_name).to_dir().resolve()

    return optimise_task(
        joined, settings, pyos_path=optimise_folder, worker_task_folder=worker_task_folder
    )


def _plams_settings(settings: Mapping) -> plams.Settings:
    """Get plams Setting from a Mapping"""
    if isinstance(settings, plams.Settings):
        return settings

    return plams.Settings(settings)
