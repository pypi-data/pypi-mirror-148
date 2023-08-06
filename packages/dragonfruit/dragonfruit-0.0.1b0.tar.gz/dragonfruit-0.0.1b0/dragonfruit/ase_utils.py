import abc
from typing import Iterable

import ase

__all__ = ("AseVisualizable", "get_visualizable")


class AseVisualizable(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_visualizable(self):
        pass


def get_visualizable(obj):
    if isinstance(obj, ase.Atoms) or (
        isinstance(obj, Iterable) and obj and all(isinstance(entry, ase.Atoms) for entry in obj)
    ):
        # ASE can iterate over this directly
        return obj
    if isinstance(obj, AseVisualizable):
        return obj.get_visualizable()
    raise TypeError(obj)
