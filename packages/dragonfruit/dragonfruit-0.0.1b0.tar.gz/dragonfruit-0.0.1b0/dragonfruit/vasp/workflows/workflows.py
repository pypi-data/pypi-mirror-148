import logging
from uuid import UUID
import typing
from abc import ABC, abstractmethod

import ase
import mincepy

from dragonfruit import mince, AseVisualizable
from dragonfruit.vasp import VaspTask, get_default_handlers, ErrorHandler

from .utils import run_with_restart

logger = logging.getLogger(__name__)

__all__ = (
    "SingleTaskWorkflow",
    "VolumeMetaConvergence",
    "ConvergenceWorkflowChain",
    "ConvergenceWorkflow",
)

_SETTINGS = typing.Dict[str, typing.Any]


class ConvergenceWorkflow(mince.Process, ABC):
    @property
    @abstractmethod
    def converged(self) -> bool:
        """Check if the workflow is converged"""

    @abstractmethod
    def run(self) -> bool:
        """Execute the workflow"""

    @property
    @abstractmethod
    def atoms(self) -> ase.Atoms:
        """Return the current final atoms objecct"""

    @property
    @abstractmethod
    def initial_atoms(self) -> ase.Atoms:
        """Return the initial atoms object"""

    @property
    @abstractmethod
    def initial_settings(self) -> _SETTINGS:
        """Return the initial settings dictionary"""

    @abstractmethod
    def create_copy(self, initial_atoms, initial_settings, *args, **kwargs):
        """Create a copy of self with new initial atoms and settings"""

    @abstractmethod
    def get_vasp_task(self) -> typing.Optional[VaspTask]:
        """Return the latest VaspTask. Returns None if it doesn't have any yet."""


class SingleTaskWorkflow(ConvergenceWorkflow, AseVisualizable):
    TYPE_ID = UUID("370a8705-d4cf-4f7b-b47e-d2e85a28576f")
    ATTRS = (
        mincepy.AsRef("_vasp_task"),
        "error_handlers",
        "description",
        mincepy.AsRef("_initial_atoms"),
        "_initial_settings",
    )

    def __init__(
        self,
        initial_atoms: ase.Atoms,
        initial_settings: dict,
        error_handlers: typing.Sequence[ErrorHandler] = get_default_handlers(),
        description: str = "",
    ):
        """Take a VASP run an run to to completion, once. Will apply error handlers
        to achieve convergence. Functionally, just a wrapper around a VaspTask, in order to
        allow being used in other "Workflow" related functions and classes.

        :param initial_atoms: Initial atoms for the workflow
        :param initial_settings: Dictionary with the VASP settings to be used
        :param error_handler: Function which registers error handlers.
            Default is to register all default vasp error handlers
        :param description: An optional description of this run
        """

        super().__init__("single-task-convergence")

        self.description = description
        self.error_handlers = error_handlers
        self._initial_atoms = initial_atoms
        self._initial_settings = initial_settings

        # Create the task, and register the error handlers
        self._vasp_task = VaspTask(self.initial_atoms, self.initial_settings)
        self.vasp_task.get_restarter().register_many(self.error_handlers)

    @property
    def vasp_task(self) -> VaspTask:
        return self._vasp_task

    def get_vasp_task(self) -> VaspTask:
        return self.vasp_task

    @property
    def atoms(self) -> ase.Atoms:
        return self.vasp_task.atoms

    @property
    def initial_atoms(self) -> ase.Atoms:
        return self._initial_atoms

    @property
    def initial_settings(self) -> dict:
        return self._initial_settings

    @property
    def converged(self) -> bool:
        """Has the workflow converged?"""
        return self.vasp_task.converged

    def run(self) -> bool:
        """Execute the workflow"""
        if self.vasp_task.done:
            logger.error("Tried to start a completed job")

        logger.info("Starting single task workflow.")
        # Execute the Vasp Task, applying the error handlers
        run_with_restart(self.vasp_task)

        self.set_result(self.converged)  # Flag object as done
        logger.info("Workflow completed. Convergende was reached: %s", self.converged)
        return self.converged

    def save_instance_state(self, saver) -> dict:
        state = super().save_instance_state(saver)
        self.update_meta(dict(converged=self.converged))
        return state

    def get_visualizable(self):
        return self.vasp_task.atoms_history

    def __str__(self):
        return "{} [converged: {}]".format(self.description, self.converged)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, super().__repr__())

    def create_copy(self, initial_atoms, initial_settings, *args, **kwargs):
        """Create a copy of self with new initial atoms and settings"""

        return self.__class__(initial_atoms, initial_settings, **kwargs)


class VolumeMetaConvergence(ConvergenceWorkflow, AseVisualizable):
    TYPE_ID = UUID("d2bdda75-9de2-488b-9d05-90f52d467f31")
    ATTRS = ("volume_threshold", "max_iter", "_task_list", "error_handlers", "description")

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        initial_atoms: ase.Atoms,
        initial_settings: dict,
        error_handlers: typing.Sequence[ErrorHandler] = get_default_handlers(),
        description: str = "",
        volume_threshold: float = 0.01,
        max_iter: int = 5,
    ):
        """Workflow to converge the relative difference in volume between two consequtive runs

        :param initial_atoms: Initial atoms for the workflow
        :param initial_settings: Dictionary with the VASP settings to be used
        :param error_handler: Function which registers error handlers.
            Default is to register all default vasp error handlers
        :param description: An optional description of this run
        :param volume_threshold: Tolerance for difference in volume fraction between
            two consequtive runs
        :param max_iter: Maximum number of iterations the workflow is allowed to do.
            Must be at least 2.
        """
        super().__init__("volume-meta-convergence")

        self.description = description
        self.error_handlers = error_handlers
        self._initial_atoms = initial_atoms
        self._initial_settings = initial_settings

        self.volume_threshold = volume_threshold
        self.max_iter = max_iter
        if max_iter < 2:
            raise ValueError(f"Too few max iterations. Should be at least 2, got {max_iter}")

        self._task_list = mincepy.builtins.RefList()  # typing.MutableSequence[VaspTask]

    @mincepy.field(attr="_initial_atoms", store_as="initial_atoms", ref=True)
    def initial_atoms(self) -> ase.Atoms:
        """Return the initial atoms of the workflow"""
        # pylint: disable=invalid-overridden-method
        return self._initial_atoms

    @mincepy.field(attr="_initial_settings", store_as="initial_settings", ref=False)
    def initial_settings(self) -> ase.Atoms:
        """Return the initial settings of the workflow"""
        # pylint: disable=invalid-overridden-method
        return self._initial_settings

    @property
    def atoms_history(self):
        """Get a list of all the atoms from this workflow (spanning all tasks)"""
        return [atoms for task in self.task_list for atoms in task.atoms_history]

    @property
    def atoms(self) -> ase.Atoms:
        if self._current_iter == 0:
            return self.initial_atoms
        return self.task_list[-1].atoms

    @property
    def task_list(self) -> typing.Sequence[VaspTask]:
        return self._task_list

    def get_vasp_task(self) -> typing.Optional[VaspTask]:
        """Return the latest VaspTask. Returns None if it doesn't have any yet."""
        if len(self.task_list) > 0:
            return self.task_list[-1]
        return None

    def _create_new_task(self) -> VaspTask:
        """Create a new VaspTask, and attach the list of error handlers"""
        if self._current_iter == 0:
            new_task = self._append_task(self.initial_atoms, self.initial_settings)
        else:
            last_task = self.task_list[-1]
            new_task = self._append_task(last_task.atoms, last_task.settings)

        new_task.get_restarter().register_many(self.error_handlers)
        return new_task

    def _append_task(self, atoms, settings) -> VaspTask:
        """Create a VaspTask and add it to the list of tasks"""
        task = VaspTask(atoms, settings)
        self._task_list.append(task)
        self.save()
        return task

    @property
    def _current_iter(self) -> int:
        return len(self.task_list)

    @property
    def converged(self) -> bool:
        """Check if the workflow is converged"""
        if self._current_iter < 2:
            # We need to have run at least twice
            return False

        # Check that we have populated both prev and current run
        cur_task = self.task_list[-1]
        prev_task = self.task_list[-2]

        if not cur_task.converged or not prev_task.converged:
            return False

        prev_vol = prev_task.atoms.get_volume()
        cur_vol = cur_task.atoms.get_volume()
        vol_ratio = abs(prev_vol - cur_vol) / prev_vol
        return bool(vol_ratio < self.volume_threshold)

    def _get_next_task(self):
        """Construct a new task, if the previous was completed or
        there was no previous task. Otherwise, return the current task, since
        it still needs to be run."""
        cur_task = self.get_vasp_task()
        if cur_task is None or cur_task.converged:
            # The current task either doesn't exist (first) iteration,
            # or it's converged
            logger.info("Creating a new VaspTask")
            return self._create_new_task()
        # Current task did not complete, and should be resumed with its internal restarters
        logger.info("Resuming from pre-existing VaspTask")
        return cur_task

    @mincepy.track
    def run(self) -> bool:
        """Run the meta converger workchain. Returns a boolean indicating if
        convergence was reached"""

        logger.info("Initiating volume convergence loop")

        while self._current_iter < self.max_iter and not self.converged:
            logger.info("Volume convergence, iteration: %d", self._current_iter)
            current_task = self._get_next_task()
            run_with_restart(current_task)

        self.set_result(self.converged)  # Flag object as done
        logger.info("After %d steps, workflow converged: %s", self._current_iter, self.converged)
        return self.converged

    def save_instance_state(self, saver) -> dict:
        state = super().save_instance_state(saver)
        self.update_meta(dict(converged=self.converged))
        return state

    def get_visualizable(self):
        return self.atoms_history

    def __str__(self):
        return "{} [{} of {}, converged: {}]".format(
            self.description, self._current_iter, self.max_iter, self.converged
        )

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, super().__repr__())

    def create_copy(self, initial_atoms, initial_settings, *args, **kwargs):
        """Create a copy of self with new initial atoms and settings"""

        return self.__class__(initial_atoms, initial_settings, **kwargs)


class ConvergenceWorkflowChain(mince.Process, AseVisualizable):
    TYPE_ID = UUID("6e8f7d41-8238-4330-9239-377e1a312359")
    ATTRS = (
        mincepy.AsRef("_workflows"),
        "workflow_args",
        "workflow_kwargs",
        "_settings_changes",
        mincepy.AsRef("_initial_atoms"),
        "_base_settings",
    )

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        initial_atoms: ase.Atoms,
        base_settings: _SETTINGS,
        settings_changes: typing.Sequence[_SETTINGS],
        workflow: typing.Callable[..., ConvergenceWorkflow] = VolumeMetaConvergence,
        workflow_args=None,
        workflow_kwargs=None,
    ):
        """Workflow which goes through a workflow with varying settings in order.

        :param initial_atoms: The initial atoms object to run on
        :param base_settings: dict, The base settings of the workflow runs.
        :param settings_changes: Sequence of dict, containing the changes to the base settings
            for each workflow. The amount of dictionaries in ``settings_changes`` determines
            the amount of workflows which will be run.
        :param workflow: A function or class which instantiates a ConvergenceWorkflow.
            The first workflow is created during instantiation of this class, and is used to
            create subsequent workflows.
        :workflow_args: Additional positional arguments to be passed to the workflow creation.
            Default: None
        :workflow_kwargs: Additional keyword arguments to be passed into the creation of a new
            workflow. Default: None
        """
        super().__init__("workflow-chain")
        self._initial_atoms = initial_atoms
        self._base_settings = base_settings
        self._workflows = mincepy.builtins.RefList()
        self.workflow_args = workflow_args or ()
        self.workflow_kwargs = workflow_kwargs or {}
        self._settings_changes = settings_changes

        # Initialize the first workflow
        settings = self.make_new_settings(self.settings_changes[0])
        initial_workflow = workflow(
            initial_atoms, settings, *self.workflow_args, **self.workflow_kwargs
        )
        self.workflows.append(initial_workflow)

    @property
    def settings_changes(self) -> _SETTINGS:
        return self._settings_changes

    @property
    def initial_atoms(self) -> ase.Atoms:
        return self._initial_atoms

    @property
    def base_settings(self) -> _SETTINGS:
        return self._base_settings

    @property
    def _current_iter(self):
        """Get index of the iteration number, starting from 0.
        Corresponds to the working index of ``settings_changes``.
        """
        return len(self.workflows) - 1

    @property
    def workflows(self):
        return self._workflows

    @property
    def atoms(self) -> ase.Atoms:
        """Return the current working atoms object"""
        return self.current_workflow.atoms

    def get_visualizable(self):
        # Get all visualizables from visualizable workflows
        return [
            vis
            for flow in self.workflows
            for vis in flow.get_visualizable()
            if isinstance(flow, AseVisualizable)
        ]

    @property
    def num_workflows(self) -> int:
        return len(self.workflows)

    @property
    def num_settings(self) -> int:
        return len(self.settings_changes)

    @property
    def current_workflow(self) -> ConvergenceWorkflow:
        """Get the current workflow for running"""
        return self.workflows[-1]

    def make_new_settings(self, changes: _SETTINGS) -> _SETTINGS:
        settings = self.base_settings.copy()
        settings.update(changes)
        return settings

    def make_new_workflow(self, settings_changes: _SETTINGS) -> ConvergenceWorkflow:
        """Make a new workflow, continuing from the final atoms of the previous workflow"""
        atoms = self.atoms
        settings = self.make_new_settings(settings_changes)

        return self.current_workflow.create_copy(
            atoms, settings, *self.workflow_args, **self.workflow_kwargs
        )

    def _iterate_workflows(self) -> typing.Iterator[ConvergenceWorkflow]:
        """Iterator function for getting every workflow. Will yield the first workflow
        which is not done, and otherwise it creates the next one and yields"""
        for index, changes in enumerate(self.settings_changes):
            try:
                # Check if we already made this workflow, and need to resume
                workflow = self.workflows[index]
            except IndexError:
                logger.info("Creating new workflow %d", index)
                # Create the workflow, and add it
                workflow = self.make_new_workflow(changes)
                self.workflows.append(workflow)
            else:
                if workflow.done:
                    logger.info("Skipping workflow %d, done.", index)
                    continue

            yield workflow

    @mincepy.track
    def run(self) -> None:
        """Execute the workflow. Will resume from the last un-completed workflow,
        if any such exist. If all workflows are done, nothing will be done.
        """
        logger.info("Starting workflow chain")
        for workflow in self._iterate_workflows():
            logger.info("Running workflow %d of %d", self.num_workflows, self.num_settings)
            workflow.run()
        self.set_result(self.converged)
        logger.info("Workflow chain done.")

    @property
    def converged(self) -> bool:
        """We only consider the workflow converged when the final workflow is converged"""
        if self.num_workflows < self.num_settings:
            # We havn't created every workflow yet
            return False
        return self.workflows[-1].converged

    def get_vasp_task(self) -> typing.Optional[VaspTask]:
        """Return the latest VaspTask. Returns None if it doesn't have any yet."""
        if self.workflows:
            return self.workflows[-1].get_vasp_task()
        return None


HISTORIAN_TYPES = (VolumeMetaConvergence, ConvergenceWorkflowChain, SingleTaskWorkflow)
