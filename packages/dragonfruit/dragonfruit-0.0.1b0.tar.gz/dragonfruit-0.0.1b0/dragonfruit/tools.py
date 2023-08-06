"""Module for pyos tools"""

import ase
import ase.db.row

try:
    import spglib
except ImportError:
    spglib = None

import pyos


def atoms_to_spglib_cell(atoms: ase.Atoms):
    return atoms.get_cell(), atoms.get_scaled_positions(), atoms.numbers


def generate_symmetry_info(atoms: ase.Atoms, symprec=0.01):
    assert spglib is not None, "Spglib is required, pip install spglib"
    spglib_cell = atoms_to_spglib_cell(atoms)
    dataset = spglib.get_symmetry_dataset(spglib_cell, symprec=symprec)
    if dataset is None:
        return {}
    # Pull out what we're interested in
    return {
        key: dataset[key]
        for key in ("number", "international", "hall", "hall_number", "pointgroup")
    }


def generate_atoms_meta(atoms: ase.Atoms):
    row = ase.db.row.AtomsRow(atoms)

    meta = {}
    for attr in ("energy", "free_energy", "fmax", "smax", "volume", "mass", "charge", "formula"):
        value = row.get(attr, None)
        if value is not None:
            meta[attr] = value

    # Let's see if we can get the spacegroup
    if spglib is not None:
        sg_info = generate_symmetry_info(atoms)
        meta["sg"] = sg_info

    return meta


def populate_atoms_meta(*one_or_more_atoms):
    """Given one or more atoms objects populate the metadata with information that makes
    them more useful for searching.

    This function can take any number of atoms objects as positional arguments.
    """
    for atoms in one_or_more_atoms:
        meta = generate_atoms_meta(atoms)
        pyos.db.update_meta(atoms, meta=meta)
