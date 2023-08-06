from typing import Sequence, Dict
from collections import Counter
import numpy as np
import ase


def make_vegard_atoms(
    atoms: ase.Atoms,
    elemental_atoms: Sequence[ase.Atoms],
    size: Sequence[int] = (1, 1, 1),
) -> ase.Atoms:
    """Apply Vegard's law, and set the lattice parameter to the pure ones.A

    https://en.wikipedia.org/wiki/Vegard%27s_law

    :param atoms: The atoms object to apply Vegard's law to
    :param elemental_atoms: Sequence of Atoms for the optimized constituents in atoms.
        May have more constituents than in the ``atoms``, but all of the constituents must be there.
        Elemental cells are assumed to be in the primitive cell with no repititions.
        Assumes the cell is of the same type, no checks will be made!
    :param size: Size of the requested atoms object, relative to to the primitive cell.
        Should be a list of 3 integers.
    """
    if len(size) != 3:
        raise ValueError(f"'size' must be of length 3, got {len(size)}")

    elemental_cells = get_elemental_cells(atoms, elemental_atoms)
    concs = get_concentrations(atoms)

    # We should only have keys from the constituents now
    assert concs.keys() == elemental_cells.keys()

    # Weighted average the lattice paramters by their concentrations
    new_cell = np.zeros((3, 3))
    for symbol, cell in elemental_cells.items():
        weight = concs[symbol]
        new_cell += weight * cell

    new_cell *= size

    new_atoms = atoms.copy()
    new_atoms.set_cell(new_cell, scale_atoms=True)
    return new_atoms


def get_elemental_cells(
    atoms: ase.Atoms, elemental_atoms: Sequence[ase.Atoms]
) -> Dict[str, ase.cell.Cell]:
    """Get the cells from the elemental atoms which corresponds to the constituents in Atoms.

    Takes in a list of elementals, and extracts the cells from the relevant elementals. E.g.
    if we pass in a NaCl atoms object, we'd get back something like
        {'Na': [[4.0, 0, 0], [0, 4, 0], [0, 0, 4]], 'Cl': [[3.8, 0, 0], [0, 3.8, 0], [0, 0, 3.8]]}
    (these are fake numbers).
    """
    # Get the constituent elements in atoms
    constituents = set(atoms.symbols)

    # Get the cells of the pure elementals for our constituents
    elemental_cells = {}

    for elem in elemental_atoms:
        elem_set = set(elem.symbols)
        # It should be an elemental, so there should only be one symbol
        if len(elem_set) != 1:
            raise ValueError(f"Elemental has {len(elem_set)} symbols, should only have 1")
        elem_sym = elem_set.pop()  # Get the symbol
        if elem_sym not in constituents:
            # Elemental is not required
            continue
        elemental_cells[elem_sym] = elem.get_cell()
        if len(elemental_cells) == len(constituents):
            # We found all of our symbols
            return elemental_cells
    # We didn't find an elemental for every constituent
    found_symbols = set(elemental_cells)
    missing_symbols = constituents - found_symbols
    raise RuntimeError(f"Missing elemental for symbol(s): {missing_symbols}")


def get_concentrations(atoms: ase.Atoms) -> Dict[str, float]:
    """Get the concentrations of each constituent."""

    counts = Counter(atoms.symbols)
    num = len(atoms)

    return {key: value / num for key, value in counts.items()}
