import logging

import mincepy

__all__ = "Process", "InvalidStateException"

logger = logging.getLogger(__name__)


class InvalidStateException(Exception):
    pass


class Process(mincepy.Process):
    ATTRS = ("_done", "_result")

    def __init__(self, name=""):
        super(Process, self).__init__(name)
        self._done = False
        self._result = None

    @property
    def done(self):
        return self._done

    def reset_state(self):
        """Reset the state back to pending and clear any results"""
        self._done = False
        self._result = None

    def set_result(self, result):
        assert not self.done, "Cannot set result, process is done"
        self._result = result
        self._done = True

    def result(self):
        if not self.done:
            raise InvalidStateException("The process is not done")

        return self._result
