import abc
import uuid
from typing import Iterable, Union, Tuple, Optional

import copy

import mincepy
import dragonfruit

__all__ = ("RunRestarter", "ErrorHandler", "PermanentFailure")


class BaseVaspError(Exception):
    """Base Vasp Error exception"""


class PermanentFailure(BaseVaspError):
    """An exception raise when an error handler detects that a situation has arisen that cannot be
    fixed"""


class ConvergenceFailure(BaseVaspError):
    """An exception raise when the calculation is not converging within the specified window"""


class ErrorHandler(mincepy.BaseSavableObject, metaclass=abc.ABCMeta):
    NAME = None
    SKIP = None  # Return value if a error handler cannot deal with it

    def __init__(self):
        super().__init__()
        assert self.NAME is not None, "Set yo name, yo'!"

    @abc.abstractmethod
    def __call__(self, vasp_task: "dragonfruit.vasp.VaspTask"):
        """Take the vasp task and create a VaspRun restart if there was an error that this handler
        could deal with"""

    @classmethod
    def accept_run(cls, restart_run: Optional["dragonfruit.vasp.VaspRun"]) -> bool:
        """Check if we want to accept the results from an error handler.
        Returns True if the returned value is OK, and otherwise False."""
        return restart_run is not cls.SKIP


class RunRestarter(mincepy.BaseSavableObject):
    """Check if vask task should execute a new run"""

    TYPE_ID = uuid.UUID("700d9498-9d3c-4c7c-ab40-29a4f86665d8")
    ATTRS = ("_all_check_functions",)

    def __init__(self):
        super().__init__()
        self._all_check_functions = []

    def create_restart(self, vasp_task):
        for _priority, handler in self._all_check_functions:
            restart_run = handler(vasp_task)
            if handler.accept_run(restart_run):
                return restart_run

        raise PermanentFailure("Can't create restart, seems no one wants to deal with the error.")

    def register(self, handler: ErrorHandler, priority=0):
        handler = copy.copy(handler)
        self._all_check_functions.append((priority, handler))
        # Higher priority should go first
        self._all_check_functions.sort(key=lambda x: x[0], reverse=True)

    def register_many(
        self, handler_params: Iterable[Union[ErrorHandler, Tuple[ErrorHandler, int]]]
    ):
        for entry in handler_params:
            if isinstance(entry, ErrorHandler):
                self.register(entry)
            else:
                # Assume it's a tuple of (handler, priority)
                handler, priority = entry
                self.register(handler, priority=priority)

    def deregister(self, name):
        to_remove = None
        for idx, handler in enumerate(self._all_check_functions):
            if handler.NAME == name:
                to_remove = idx
        if to_remove is not None:
            del self._all_check_functions[to_remove]


HISTORIAN_TYPES = (RunRestarter,)
