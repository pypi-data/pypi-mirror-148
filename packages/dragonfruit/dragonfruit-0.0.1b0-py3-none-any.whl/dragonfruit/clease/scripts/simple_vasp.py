import logging
from pathlib import Path
from typing import Sequence
import uuid
import shutil

import pymongo
import mincepy
import minkipy
import pyos
from pyos import psh

import dragonfruit as df
from dragonfruit import vasp
from dragonfruit.vasp.workflows import run_with_restart

__all__ = "run_clease_pyos", "run_clease_pyos_workflow", "RunWorkflow"

logger = logging.getLogger("dragonfruit.clease.scripts")


def run_clease_pyos(vasp_task: df.vasp.VaspTask, group: str):

    logger.info("Running on task %s", vasp_task.obj_id)

    path = pyos.Path("vasp_task_{}/".format(vasp_task.obj_id))
    context = pyos.pathlib.working_path(path)
    curpath = Path(".").resolve()
    logger.info("Pyos subdirectory: %s", path)
    logger.info("Running in directory: %s", curpath)

    with context:
        # Run the task, and update the project at the end
        run_with_restart(vasp_task)

        final_atoms = vasp_task.atoms
        logger.info("Final atoms %s", final_atoms)
        meta = dict(converged=vasp_task.converged, crashed=vasp_task.crashed)
    # Move into the directory
    df.clease.set_final(
        final_atoms, vasp_task.initial_atoms, group, meta=meta, directory=pyos.os.getcwd()
    )


def finalize(workflow, group: str, clease_initial=None, extra_files: Sequence = None):
    converged = workflow.converged
    if converged:
        logger.info("Finalizing workflow")
        _finalize_converged(workflow, group, clease_initial=clease_initial, extra_files=extra_files)
        logger.info("Finalization complete.")
    else:
        logger.warning("Workflow did not converge. Nothing further will be done to this task.")


def _finalize_converged(workflow, group: str, clease_initial=None, extra_files: Sequence = None):
    """Helper function for performing the finalization of a *converged* workflow"""
    converged = workflow.converged
    assert converged

    vasp_task = workflow.get_vasp_task()

    final_atoms = vasp_task.atoms
    logger.info("Final atoms %s", final_atoms)
    crashed = vasp_task.crashed
    meta = dict(converged=converged, crashed=crashed)

    # Workflow converged, set the final atoms
    logger.info("Setting final atoms")
    if clease_initial is None:
        clease_initial = workflow.initial_atoms
        initial_meta = pyos.db.get_meta(psh.oid(clease_initial))
        clease_initial_id = initial_meta.get(df.clease.Meta.CLEASE_INITIAL, None)
        if clease_initial_id:
            logger.info("Found clease initial in metadata, initial id: %s", clease_initial_id)
            clease_initial = psh.load(clease_initial_id)
        else:
            logger.info(
                "Using workflow initial atoms as clease initial, id: %s", psh.oid(clease_initial)
            )

    df.clease.set_final(
        final_atoms, clease_initial, group=group, meta=meta, directory=pyos.os.getcwd()
    )  # Move into the directory

    if extra_files is not None:
        logger.info("Storing extra files.")
        _copy_extra_files(final_atoms, extra_files)


def _copy_extra_files(atoms, extra_files: Sequence):
    """Copy extra files from PWD into the database,
    and save the obj id in the atoms metadata.
    """
    hist = mincepy.get_historian()
    pyos_dir = pyos.os.getcwd()
    run_path = Path(".")
    extra_files_meta = {}
    for filename in extra_files:
        # Read the file from disk, assuming PWD as working directory
        file_path = run_path / filename
        logger.info("Storing file: %s", filename)
        try:
            with open(file_path, "rb") as disk_stream:
                # New file
                db_file = hist.create_file(filename=filename)

                with db_file.open("wb") as db_stream:
                    shutil.copyfileobj(disk_stream, db_stream)

            # Save the db_file, store it in a separate subfolder
            pyos.db.save_one(db_file, pyos_dir)
            pyos.psh.mv(db_file, "extra_files/")
            # Link the file oid to the final atoms meta data
            oid = str(psh.oid(db_file))
            extra_files_meta[filename] = oid

        except FileNotFoundError:
            logger.error("Extra file %s not found. Skipping.", file_path.resolve())

    # Add the extra files to the final atoms metadata
    if extra_files_meta:
        logger.info(
            "Adding following extra_files metadata to the final atoms: %s", extra_files_meta
        )
        pyos.db.update_meta(atoms, meta={"extra_files": extra_files_meta})
    else:
        logger.error("No extra files metadata was added.")


def run_clease_pyos_workflow(
    workflow,
    group: str,
    clean_large_files=True,
    clease_initial=None,
    print_level=logging.INFO,
    extra_files: Sequence = None,
):
    """The extra_files allows to copying extra files from the working directory.
    The file objid is also added to the final atoms
    """

    with df.utils.log_to_stdout(log_level=print_level):
        # Print some useful information about the job in the log
        logger.info("### STARTING NEW RUN ###")

        logger.info("Meta convergence workflow: %s", workflow.name)

        path = pyos.Path("workflows/vasp_workflow_{}/".format(workflow.obj_id))
        curpath = Path(".").resolve()
        logger.info("Pyos directory: %s", path.resolve())
        logger.info("Running in directory: %s", curpath)

        # Get latest task which references this workflow
        hist = df.get_historian()
        try:
            graph = hist.references.get_obj_ref_graph(
                hist.get_obj_id(workflow), direction=mincepy.INCOMING
            )
        except pymongo.errors.BulkWriteError as exc:
            logger.error("Tried to locate references, but encountered a pymongo error: %s", exc)
        else:
            objs = tuple(
                hist.find(
                    obj_id=list(graph.nodes),
                    sort={mincepy.records.CREATION_TIME: mincepy.ASCENDING},
                    obj_type=minkipy.tasks.Task,
                )
            )
            if objs:
                logger.info(
                    "Minkipy tasks which references this workflow, in ascending order:\n%s",
                    tuple(map(psh.oid, objs)),
                )
            else:
                logger.warning("Found no minkipy tasks which references this workflow.")

        try:
            # Main part of the execution
            with pyos.pathlib.working_path(path):
                logger.info("Executing workflow.")
                workflow.run()
                converged = workflow.converged
                logger.info("Workflow done. Converged: %s", converged)

            # Do some finalization, like saving the final atoms if we converged
            finalize(workflow, group, clease_initial=clease_initial, extra_files=extra_files)

            logger.info("Task complete.")

        finally:
            if clean_large_files:
                logger.info("Cleaning large data files")
                vasp.clean_large_vasp_files(curpath)


class RunWorkflow(mincepy.BaseSavableObject):
    """
    NOTE: This object is now deprecated. It is kept for legacy reasons and for loading.
    Passing kwargs is now directly supposed in minkiPy.

    Helper object to initialize a run_clease_pyos_workflow with kwargs. Usage:

    runner = RunWorkflow(print_level=logging.INFO)
    minkipy.task(runner.run, ...)
    """

    ATTRS = ("clean_large_files", "print_level", "clease_initial")
    TYPE_ID = uuid.UUID("c875b739-97b4-4fd7-83d3-674337dba978")

    def __init__(self, clean_large_files=True, clease_initial=None, print_level=logging.INFO):
        super().__init__()
        self.clean_large_files = clean_large_files
        self.clease_initial = clease_initial
        self.print_level = print_level

    def run(self, workflow, group):
        run_clease_pyos_workflow(
            workflow,
            group,
            clean_large_files=self.clean_large_files,
            clease_initial=self.clease_initial,
            print_level=self.print_level,
        )


HISTORIAN_TYPES = (RunWorkflow,)
