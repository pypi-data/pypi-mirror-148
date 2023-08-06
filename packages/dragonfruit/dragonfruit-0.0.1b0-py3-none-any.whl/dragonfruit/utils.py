import os
import sys
import logging
import contextlib

try:
    from contextlib import nullcontext
except ImportError:
    # for Py<3.7
    from contextlib2 import nullcontext
from collections import deque
import importlib
from pathlib import Path
from typing import Tuple, Dict, Sequence, TypeVar
import copy

import ase
from ase.calculators.singlepoint import SinglePointCalculator
import numpy as np

from dragonfruit import get_historian

_T = TypeVar("T")


def log_to_stdout(log_level=logging.INFO):
    @contextlib.contextmanager
    def _log_to_stdout():
        logger = logging.getLogger("dragonfruit")  # Only capture dragonfruit logs
        logger.setLevel(log_level)

        original_level = None
        if logger.level > log_level:
            original_level = logger.level
            logger.setLevel(log_level)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        formatter = logging.Formatter("%(asctime)s: %(message)s", "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        try:
            logger.addHandler(handler)
            yield
        finally:
            logger.removeHandler(handler)
            if original_level is not None:
                logger.setLevel(original_level)

    if not log_level:
        return nullcontext()
    return _log_to_stdout()


def get_atoms_sort_map(atoms):
    """Ensure all atoms in the array are sorted"""
    # We just need the order of occurrence of the symbols
    # Sorting groups in order of occurrence
    symbols = []
    for symbol in atoms.symbols:
        if symbol not in symbols:
            symbols.append(symbol)

    nat = len(atoms)
    sort = []
    index = np.array(range(nat))

    # Sorting list
    for symbol in symbols:
        for i in index[atoms.symbols == symbol]:
            sort.append(int(i))

    # Resorting
    resort = list(range(nat))
    for i in range(nat):
        resort[sort[i]] = i
    return sort, resort


def copy_one(obj: _T, hist=None) -> _T:
    """Copy a single object with the historian. Will fallback to python copy, if no historian
    is found"""
    if hist is None:
        hist = get_historian()
    copyer = hist.copy if hist else copy.copy
    return copyer(obj)


def copy_many(seq: Sequence[_T], hist=None) -> Sequence[_T]:
    """Copy multiple objects with the historian. Will fallback to python copy, if no historian
    is found"""
    if hist is None:
        hist = get_historian()
    return [copy_one(obj, hist=hist) for obj in seq]


def resort_atoms_and_results(atoms, resort) -> Tuple[ase.Atoms, Dict]:
    """Sort an atoms object and the corresponds arrays which will be returned in a
    results dictionary along with the atoms"""
    hascalc = bool(atoms.calc)
    if atoms.calc:
        results = atoms.calc.results.copy()
    else:
        results = {}
    sorted_atoms = atoms.copy()[resort]  # Removes the calculator and results
    # Fix calculator results
    results_arrays = ("forces", "magmoms")  # Results in arrays for resorting

    for array in results_arrays:
        if array in results:
            results[array] = results[array][resort]
    if hascalc:
        # Reattach new singlepoint calculator with sorted results
        newcalc = SinglePointCalculator(sorted_atoms, **results)
        sorted_atoms.calc = newcalc
    return sorted_atoms, results


def is_string_in_file(filename, string):
    if Path(filename).is_file():
        with open(filename, "r") as file:
            for line in file:
                if string in line:
                    return True
    return False


@contextlib.contextmanager
def working_directory(path):
    """Changes working directory and returns to previous on exit."""
    prev_cwd = Path.cwd()
    os.chdir(str(path))  # str call for python < 3.6
    try:
        yield
    finally:
        os.chdir(str(prev_cwd))


def load_module(fullname):
    parts = fullname.split(".")

    # Try to find the module, working our way from the back
    mod = None
    remainder = deque()
    for _ in range(len(parts)):
        try:
            mod = importlib.import_module(".".join(parts))
            break
        except ImportError:
            remainder.appendleft(parts.pop())

    if mod is None:
        raise ValueError("Could not load a module corresponding to '{}'".format(fullname))

    return mod, remainder


def load_object(fullname):
    """
    Load a class from a string
    """
    obj, remainder = load_module(fullname)

    # Finally, retrieve the object
    for name in remainder:
        try:
            obj = getattr(obj, name)
        except AttributeError:
            raise ValueError("Could not load object corresponding to '{}'".format(fullname))

    return obj


@contextlib.contextmanager
def null_context():
    """Context that does nothing"""
    yield
