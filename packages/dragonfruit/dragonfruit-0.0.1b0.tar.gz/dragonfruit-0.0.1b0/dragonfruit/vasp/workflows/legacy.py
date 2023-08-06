import logging
import uuid
import abc

import mincepy

from dragonfruit import mince
from dragonfruit.vasp import VaspTask

from .utils import run_with_restart

logger = logging.getLogger(__name__)

__all__ = ("LegacyWorkflow", "LegacyVolumeMetaConvergence")


class LegacyWorkflow(mince.Process, metaclass=abc.ABCMeta):
    """Base Workflow class"""

    TYPE_ID = uuid.UUID("4569c8eb-d26c-4e3f-9df5-1278a03b5791")
    ATTRS = ("_vasp_task", "description")

    def __init__(self, name, vasp_task: VaspTask, description=""):
        super().__init__(name)
        self._vasp_task = vasp_task
        self.description = description

    @property
    def vasp_task(self):
        return self._vasp_task

    @abc.abstractmethod
    def run(self):
        pass


class LegacyVolumeMetaConvergence(LegacyWorkflow):
    """Workflow to converge the relative difference in volume between
    two consequtive runs"""

    TYPE_ID = uuid.UUID("2d6dbaeb-c0b5-4109-9f59-76ca4f13ff9b")
    ATTRS = ("volume_threshold", "max_iter", "_current_iter", "_previous_run", "_current_run")

    def __init__(
        self, vasp_task: VaspTask, description="", volume_threshold: float = 0.01, max_iter: int = 5
    ):
        super().__init__("volume-meta-convergence", vasp_task, description=description)
        self.volume_threshold = volume_threshold
        self.max_iter = max_iter
        self._current_iter = 0  # Current iteration count
        self._current_run = vasp_task.get_last_run()
        self._previous_run = None

    @property
    def converged(self) -> bool:
        if self._previous_run is None or self._current_run is None:
            return False

        prev_vol = self._previous_run.atoms.get_volume()
        cur_vol = self._current_run.atoms.get_volume()

        vol_ratio = abs(prev_vol - cur_vol) / prev_vol
        return bool(vol_ratio < self.volume_threshold)

    @mincepy.track
    def run(self) -> bool:
        """Run the meta converger workchain. Returns a boolean indicating if
        convergence was reached"""

        while self._current_iter < self.max_iter and not self.converged:
            self._current_iter += 1
            # Make current -> previous, and current -> new run
            self._previous_run, self._current_run = (
                self._current_run,
                run_with_restart(self.vasp_task),
            )

        self.set_result(self.converged)  # Flag object as done
        return self.converged

    def __str__(self):
        return "{} [{} of {}, converged: {}]".format(
            self.description, self._current_iter, self.max_iter, self.converged
        )


HISTORIAN_TYPES = (
    LegacyWorkflow,
    LegacyVolumeMetaConvergence,
)
