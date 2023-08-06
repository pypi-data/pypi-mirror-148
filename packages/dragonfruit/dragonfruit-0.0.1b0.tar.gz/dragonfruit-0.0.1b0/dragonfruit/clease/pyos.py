from typing import Optional, Mapping, Sequence, Union, Callable
import copy
import logging

import ase
import ase.db
import clease
import mincepy
import pyos
from pyos import psh
import tqdm
import minkipy

import dragonfruit as df
import dragonfruit.vasp.workflows as wf
from dragonfruit import pyos_utils

from . import paths
from . import scripts
from . import utils

__all__ = (
    "Meta",
    "init",
    "init_bulk",
    "root",
    "get_structure_settings",
    "create_settings",
    "populate_database",
    "get_atoms",
    "new_endpoints",
    "new_random_structures",
    "set_final",
    "set_initial",
    "internal_path",
    "import_ase_db",
    "get_settings",
    "save_settings",
    "submit_structures",
    "submit_workflow",
    "paths",
)

logger = logging.getLogger(__name__)

DEFAULT_FINAL = "final"
INITIAL = "initial"


# Metadata keys
class Meta:
    CLEASE_GROUP = "clease_group"
    CLEASE_INITIAL = "clease_initial"
    CLEASE_FINAL = "clease_final"


def save_settings(settings, settings_name: str) -> mincepy.Dict:
    path = pyos.Path(internal_path() / settings_name)
    if isinstance(settings, dict):
        settings = mincepy.Dict(settings)
    return pyos.db.save_one(settings, path, overwrite=True)


def get_settings(settings_name: str) -> mincepy.Dict:
    path = internal_path() / settings_name

    if not path.exists():
        # Create a new dictionary, and save it
        settings = mincepy.Dict()
        # Create the dict on the server, and give it the metadata
        save_settings(settings, path)
    else:
        settings = pyos.psh.load(path)
    return settings


def init(message="This is a CLEASE project"):
    """Initialise a new CLEASE project with an optional message.
    Will create a simple README file"""
    path = pyos.Path(paths.CLEASE_DIR / "README")
    if path.exists():
        raise RuntimeError(
            "The CLEASE directory already exists. "
            f"If you want to reinitialize, first remove {path}"
        )

    readme = mincepy.get_historian().create_file("README")
    readme.write_text(message)
    pyos.db.save_one(readme, path, overwrite=True)


def init_bulk(crystalstructure, a: float, c: float = None, covera: float = None, u: float = None):
    # Set up the project dictionary
    init(message="This is a bulk CLEASE project.")

    settings = mincepy.Dict(type="CEBulk", crystalstructure=crystalstructure, a=a)
    if c is not None:
        settings["c"] = c
    if covera is not None:
        settings["covera"] = covera
    if u is not None:
        settings["u"] = u

    settings_path = internal_path() / paths.STRUCTURE_SETTINGS
    if settings_path.exists():
        current_settings = pyos.psh.load(settings_path)
        if current_settings != settings:
            raise RuntimeError(
                "A clease repository already exists. "
                f"If you want to reinitialise first remove {settings_path}"
            )

    save_settings(settings, paths.STRUCTURE_SETTINGS)
    return settings


def internal_path() -> pyos.Path:
    """Path to where settings and other project related things are stored"""
    return root() / paths.CLEASE_DIR


def root() -> pyos.Path:
    """Find the root folder of the clease project"""
    path = psh.pwd()
    if paths.CLEASE_DIR in psh.ls(path):
        return path

    while path != pyos.Path("/"):
        path = (path / "..").resolve().to_dir()  # Move up one
        if paths.CLEASE_DIR in psh.ls(path):
            return path
        # repeat...

    raise RuntimeError(
        "fatal: not a clease repository (or any of the parent directories): {}".format(
            paths.CLEASE_DIR
        )
    )


def get_structure_settings() -> Mapping:
    """Get the structure settings from the clease root"""
    return get_settings(paths.STRUCTURE_SETTINGS)


def create_settings(
    init_args: Optional[dict] = None, final_group: Optional[str] = None
) -> clease.settings.ClusterExpansionSettings:
    """Create cluster expansion settings.  The resulting settings will have a database
    populated with all the initial structures along with any final structure if a final_group
    is specified.

    :param init_args: optional init arguments to be passed when constructing the clease settings
    :param final_group: the name a group to use as the 'final' structures inserted into the
        created database
    """
    ce_settings = None
    init_args = init_args or {}
    struct_settings = get_structure_settings()

    if struct_settings["type"] == "CEBulk":
        settings = dict(struct_settings)

        settings.pop("type")
        init_args.update(settings)
        ce_settings = clease.settings.CEBulk(**init_args)

    if ce_settings is None:
        raise TypeError("Don't know how to construct '{}'".format(struct_settings["type"]))

    populate_database(ce_settings, 0, final_group)
    return ce_settings


def populate_database(
    settings: clease.settings.ClusterExpansionSettings, generation_number=0, final_group: str = None
):
    """Given a clease database this call will populate it with initial structures and optionally
    corresponding final structures inserting into a given generation of an existing cluster
    settings."""
    initials = get_atoms(INITIAL)
    project_root = root()

    # Now let's try and match up initial and final
    if final_group:
        # Go through finding the final structure that corresponds to each initial
        finals = []
        with tqdm.tqdm(psh.oid(*initials), desc="Fetching") as obj_ids:
            for obj_id in obj_ids:
                results = psh.find(
                    project_root,
                    type=ase.Atoms,
                    meta={Meta.CLEASE_GROUP: final_group, Meta.CLEASE_INITIAL: obj_id},
                )

                if results:
                    finals.append(psh.load(results[0]))
                    if len(results) > 1:
                        logger.warning(
                            "More than one final atoms found corresponding to initial '{}'".format(
                                obj_id
                            )
                        )
                else:
                    finals.append(None)
    else:
        finals = [None] * len(initials)

    inserter = clease.NewStructures(
        settings=settings, struct_per_gen=len(initials), generation_number=generation_number
    )

    # Insert all the existing structures into the database
    for initial, final in zip(initials, finals):
        inserter.insert_structure(initial, final)


def get_atoms(group: str = INITIAL, initial=None, final_only=False) -> Sequence[ase.Atoms]:
    """Get all the atoms in a particular clease group.  Defaults to initial structures"""
    meta = {Meta.CLEASE_GROUP: group}
    if initial:
        if not isinstance(initial, (list, tuple)):
            initial = [initial]
        hist = mincepy.get_historian()
        initial_obj_id = (hist.to_obj_id(obj) for obj in initial)
        meta.update({Meta.CLEASE_INITIAL: mincepy.q.in_(*initial_obj_id)})
    if final_only:
        meta.update({Meta.CLEASE_FINAL: True})

    nodes = psh.find(root(), type=ase.Atoms, meta=meta)
    if nodes is None:
        return []
    images = psh.load(nodes)
    if isinstance(images, ase.Atoms):
        images = [images]

    if final_only and initial is not None:
        if len(images) > len(initial):
            logger.warning(
                "Only final images were requested for %d initial images, but %d were found",
                len(initial),
                len(images),
            )

    return images


def new_endpoints(
    concentration: clease.settings.Concentration, directory: pyos.os.PathSpec = None
) -> Sequence[ase.Atoms]:
    with utils.clease_temporary_database() as clease_db:
        settings = create_settings(
            init_args=dict(
                size=(1, 1, 1),
                concentration=concentration,
                db_name=clease_db.name,
                # Set these to speed things up because clease will internally generate big
                # enough supercells to accommodate clusters of this size (and then throw them away)
                max_cluster_dia=[5],
            )
        )

        # Now generate the pool
        structure_generator = clease.NewStructures(settings=settings, generation_number=1)
        structure_generator.generate_conc_extrema()
        # Connect to the database
        ase_db = ase.db.connect(clease_db.name)

        structures = []
        for row in ase_db.select(gen=1):
            atoms = row.toatoms()  # type: ase.Atoms
            set_initial(atoms, directory=directory)
            # Add it ot the dict to return
            structures.append(atoms)

        return structures


def new_random_structures(
    num_to_generate=1, directory: pyos.os.PathSpec = None, **kwargs
) -> Sequence[ase.Atoms]:
    """
    Create structures that are different from any other that is currently in the database

    :param num_to_generate: the number of random structures to generate
    :param kwargs: these are passed to the crystal structure setting constructor along with the
        settings currently held in self.settings
    """

    with utils.clease_temporary_database() as clease_db:
        kwargs["db_name"] = clease_db.name
        settings = create_settings(init_args=kwargs)

        structure_generator = clease.NewStructures(
            settings=settings, struct_per_gen=num_to_generate, generation_number=1
        )

        # Generate all the structures
        structure_generator.generate_random_structures()

        # Get the structure from the database
        ase_db = ase.db.connect(clease_db.name)
        structures = []
        for row in ase_db.select(gen=1):
            atoms = row.toatoms()
            pyos.db.save_one(atoms)
            set_initial(atoms, directory=directory)
            structures.append(atoms)

        return structures


def set_final(
    final: ase.Atoms,
    initial: ase.Atoms,
    group: str = DEFAULT_FINAL,
    directory: pyos.os.PathSpec = None,
    meta: dict = None,
):
    """Set a structure as the final structure for a given initial"""
    logger.debug("Setting final in group %s", group)
    obj_id = pyos.db.save_one(final)
    if directory is not None:
        directory = pyos.Path(directory).to_dir()
        logger.debug("Moving final to directory: %s", directory)
        pyos.psh.mv(obj_id, directory)
    if meta is None:
        meta = {}
    meta = pyos_utils.sanitize_meta(meta)

    # Check if any final exists for the initial in this group already:
    other_finals = get_atoms(group=group, initial=initial, final_only=True)
    if len(other_finals) > 1:
        logger.warning(
            "Expected to find at most 1 final atoms object, but got %d", len(other_finals)
        )
    for atoms in other_finals:
        logger.debug("Removing final tag from %d", psh.oid(atoms))
        other_meta = pyos.db.get_meta(psh.oid(atoms))
        other_meta.pop(Meta.CLEASE_FINAL)
        pyos.db.set_meta(atoms, meta=other_meta)

    final_meta = {
        Meta.CLEASE_INITIAL: psh.oid(initial),
        Meta.CLEASE_GROUP: group,
        Meta.CLEASE_FINAL: True,
    }
    # This will cause keys to collide if they overlap
    final_meta = dict(**final_meta, **meta)
    # Update atoms object related metadata
    final_meta.update(df.tools.generate_atoms_meta(final))

    # Set the metadata accordingly
    pyos.db.update_meta(final, meta=final_meta)
    logger.debug("New meta for final: %s", pyos.db.get_meta(psh.oid(final)))


def set_initial(initial: ase.Atoms, directory: Union[str, pyos.PurePath] = None, meta: dict = None):
    """Set initial atoms.  No uniqueness check is made by this call"""
    obj_id = pyos.db.save_one(initial)
    if directory is not None:
        directory = pyos.Path(directory).to_dir()
        pyos.psh.mv(obj_id, directory)
    if meta is None:
        meta = {}
    meta = pyos_utils.sanitize_meta(meta)
    meta.update(df.tools.generate_atoms_meta(initial))  # Update atoms object related metadata
    pyos.db.update_meta(initial, meta={Meta.CLEASE_GROUP: INITIAL, **meta})


def import_ase_db(
    name: str,
    group: str = DEFAULT_FINAL,
    initial_directory: pyos.os.PathSpec = None,
    final_directory: pyos.os.PathSpec = None,
):
    db = ase.db.connect(name)
    mapping = {}  # Mapping: initial id -> final id
    initials = {}
    finals = {}

    with tqdm.tqdm(tuple(db.select()), desc="loading") as rows:
        for row in rows:
            atoms = row.toatoms()
            if "final_struct_id" in row:
                # We have an initial structure
                mapping[row.id] = row.final_struct_id
                initials[row.id] = atoms
            else:
                finals[row.id] = atoms

            obj_id = pyos.db.save_one(atoms)
            name = row.key_value_pairs.get("name", None)
            if name is not None:
                meta = df.tools.generate_atoms_meta(atoms)
                meta["import_name"] = name
                pyos.db.set_meta(obj_id, meta=meta)

    with tqdm.tqdm(initials.values(), desc="import initials") as with_progress:
        for initial in with_progress:
            set_initial(initial, directory=initial_directory)

    with tqdm.tqdm(mapping.items(), desc="importing finals") as with_progress:
        for initial_id, final_id in with_progress:
            try:
                set_final(
                    finals[final_id], initials[initial_id], group=group, directory=final_directory
                )
            except KeyError:
                print("Error: failed to find final for initial with id '{}'".format(initial_id))


def submit_structures(
    structures: Union[ase.Atoms, Sequence[ase.Atoms]],
    group: str,
    command=None,
    log_level=logging.INFO,
    **kwargs,
) -> Sequence[int]:
    """Submit structures using the settings and group settings.

    :param structures: Atoms or list of Atoms to be submitted
    :param group: Name of the group settings to be used
    :param command: The function or string to be passed into the minkipy task
    :param kwargs: These are passed as overrides to the VASP settings dictionary
    """
    if command is None:
        command = scripts.run_clease_pyos

    settings = dict(get_settings(paths.GENERAL_SETTINGS))
    group_settings = get_settings(paths.GROUP_SETTINGS)

    settings.update(group_settings.get(group, {}))
    settings.update(kwargs)

    if isinstance(structures, ase.Atoms):
        structures = [structures]

    task_ids = []

    with pyos.pathlib.working_path(pyos.Path(group).to_dir()):
        for atoms in structures:
            # We may mutate settings, so use copy
            # dict, as we are likely a mincepy.Dict object
            atoms_settings = copy.deepcopy(settings)

            vasp_task = df.vasp.VaspTask(atoms, atoms_settings)
            restarter = vasp_task.get_restarter()
            handlers = df.vasp.get_default_handlers()
            restarter.register_many(handlers)

            task = minkipy.task(
                command, args=(vasp_task, group), folder=f"vasp_task_{psh.oid(atoms)}_{group}"
            )
            task.log_level = log_level
            task_id = task.save()

            minkipy.queue().submit(task)
            task_ids.append(task_id)

    return task_ids


def submit_workflow(
    *structures: ase.Atoms,
    group: str = DEFAULT_FINAL,
    command=scripts.run_clease_pyos_workflow,
    command_kwargs: dict = None,
    dynamic=True,
    workflow_factory: Callable = wf.VolumeMetaConvergence,
    workflow_kwargs: dict = None,
    log_level=logging.INFO,
    extra_settings: dict = None,
    queue_name: str = None,
    skip_duplicate_check: bool = False,
) -> Sequence[int]:
    """Submit structures using the settings and group settings.

    :param structures: Atoms or list of Atoms to be submitted
    :param group: Name of the group settings to be used
    :param command: The function or string to be passed into the minkipy task
    :param command_kwargs: kwargs passed into the command option in the minkipy task.
        Default: {}
    :param dynamic: Should the command be imported dynamically at runtime,
        or statically passed at creation time.
        For more information, see the documentaiton for minkipy.Task
    :param workflow_factory: Workflow factory to be executed in the Task.
        Should take "atoms" and "atoms_settings" as positional arguments.
    :param workflow_kwargs: Dictionary of key-value pairs to be passed on to the workflow class
    :param log_level: Level for the logger capture in the minkipy Task.
        Default: logging.INFO
    :param extra_settings: Dictionary with extra VASP settings. Overwrites default keys.
        Default: {}
    :param queue_name: Name of the minki queue for submission.
        Default: None
    :param skip_duplicate_check: forgo checking the queue for duplicate tasks?
        For more information, see the documentation for mincepy.Queue.submit.
        Default: False
    """

    command_kwargs = command_kwargs or {}
    extra_settings = extra_settings or {}
    workflow_kwargs = workflow_kwargs or {}

    settings = dict(get_settings(paths.GENERAL_SETTINGS))
    group_settings = get_settings(paths.GROUP_SETTINGS)

    settings.update(group_settings.get(group, {}))
    settings.update(extra_settings)

    tasks = []
    queue = minkipy.queue(queue_name)

    with pyos.pathlib.working_path(pyos.Path(group).to_dir()):
        for atoms in structures:
            if not isinstance(atoms, ase.Atoms):
                raise TypeError(f"Got a structure which is not an atoms object: {atoms}")
            # We may mutate settings, so use copy
            # dict, as we are likely a mincepy.Dict object
            atoms_settings = copy.deepcopy(settings)

            converger = workflow_factory(atoms, atoms_settings, **workflow_kwargs)

            # Working directory for the task
            folder = f"workflows/vasp_task_{psh.oid(atoms)}_{group}"

            task = minkipy.task(
                command,
                args=(converger, group),
                kwargs=command_kwargs,
                dynamic=dynamic,
                folder=folder,
            )
            task.log_level = log_level

            queue.submit(task, skip_duplicate_check=skip_duplicate_check)
            tasks.append(task)

    return tasks
