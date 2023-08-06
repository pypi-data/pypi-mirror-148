import logging
import dragonfruit as df

from dragonfruit.vasp import VaspTask, VaspRun

logger = logging.getLogger(__name__)

__all__ = ("run_with_restart", "create_restart", "create_next_run")


def is_initial(vasp_task: VaspTask) -> bool:
    """Does the vasp_task have any previous runs?"""
    return len(vasp_task.runs) == 0


def run_with_restart(vasp_task: VaspTask) -> VaspRun:
    """Run a vasp task, applying the restarters until convergence or a failure
    Returns the final VaspRun object, which achieved convergence"""
    logger.info("-- Running vasp task to convergence --")

    initial = is_initial(vasp_task)
    logger.info("Is run initial? %s", initial)

    try:
        # We may need to apply restarters on a vasp_task which has already been running
        current_run = create_next_run(vasp_task)
        if initial:
            # If we're an initial run, we first need to run, before we can
            # apply restarters
            current_run = vasp_task.new_run()
            logger.info("Executing new run")
            vasp_task.execute_run(current_run)
        logger.info("Entering main convergence loop")
        restart_counter = 0
        while not current_run.converged:
            # Do a restart
            restart_counter += 1
            logger.info("Running restart iteration %d", restart_counter)
            current_run = create_restart(vasp_task)
            vasp_task.execute_run(current_run)
    except df.vasp.PermanentFailure as exc:
        logger.error("There was a catastrophic failure, I'm out:\n%s", exc)
        raise
    logger.info("-- Convergence was reached --")
    return current_run


def create_next_run(vasp_task: VaspTask) -> VaspRun:
    """Create a new VaspRun, either by constructing a new VaspRun on the initial,
    or applying restarters on the latest vasp_run"""
    initial = is_initial(vasp_task)
    if initial:
        logger.info("Creating new initial run.")
        return vasp_task.new_run()
    return create_restart(vasp_task)


def create_restart(vasp_task: VaspTask) -> VaspRun:
    """Apply the restarter objects from a VaspTask, and return a new VaspRun"""
    logger.info("Creating new VaspRun from restarters")
    restarter = vasp_task.get_restarter()
    restart = restarter.create_restart(vasp_task)
    vasp_task.append_run(restart)
    return restart
