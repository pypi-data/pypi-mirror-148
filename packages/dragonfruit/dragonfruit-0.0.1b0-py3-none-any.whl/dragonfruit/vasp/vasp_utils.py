import logging
from pathlib import Path
import numpy as np
import ase.units as units
from ase import Atoms

__all__ = ("is_stress_converged", "is_relaxation", "is_converged", "clean_large_vasp_files")

logger = logging.getLogger(__name__)

DEFAULT_LARGE_FILES = ("WAVECAR", "CHGCAR", "CHG", "PROCAR")


def clean_large_vasp_files(curpath, remove=DEFAULT_LARGE_FILES):
    curpath = Path(curpath)
    for file in remove:
        file = curpath / file
        try:
            file.unlink()
            logger.info("File removed: %s", str(file))
        except FileNotFoundError:
            logger.info("Did not find file: %s", str(file))
        except OSError as exception:
            logger.error('Could not remove file "%s" due to exception: %s', str(file), exception)


def is_stress_converged(atoms: Atoms, ediffg: float, isif: int, tol: float = 0.01) -> bool:
    """Read if stress tensor would be considered converged - this is a little more tricky,
    as VASP won't explicitly tell us how they do it - requires a bit of re-calculations based on the
    vasp source code.
    A tolerance is used to accept a bit of numerical noise, due to conversions."""

    # We don't have stress for some reason. Why not?
    if "stress" not in atoms.calc.results:
        msg = "I don't have a stress tensor. Cannot tell you if the stress is ok!"
        raise ValueError(msg)

    stress = atoms.get_stress()
    # Undo the unit conversions done in ASE
    stress *= -1 / units.GPa / 1e-1
    # Recalculate the stress to the value used internally in VASP
    # I don't know why ASE uses _e
    # pylint: disable=protected-access
    fakt = units._e * 1e22 / atoms.get_volume()  # VASP conversion into kB - we need to undo it
    stress /= fakt

    if isif == 3:
        return (stress / len(atoms) < (abs(ediffg) + tol)).all()
    if isif == 7:
        # TODO: account for pstress
        # Something is slightly off...
        press = stress[:3].sum() / 3
        print(press)
        return press / len(atoms) < abs(ediffg)

    raise NotImplementedError


def is_relaxation(settings) -> bool:
    return settings.get("ibrion", -1) in [1, 2, 3] and settings.get("nsw", 0) > 0


def is_converged(atoms_history, settings) -> bool:
    """Check that the current results are converged as defined in according to the settings"""
    # pylint: disable=too-many-return-statements
    last_atoms = atoms_history[-1]
    if not last_atoms.calc:
        return False

    last_results = last_atoms.calc.results

    # We don't have results
    if "forces" not in last_results and "energy" not in last_results:
        return False

    # Check if SCF converged
    scf = last_atoms.info.get("scf_converged", None)
    # We skip if we haven't stored 'scf_converged'
    if scf is False:
        return False

    if is_relaxation(settings):
        # Check geometry criteria

        # VASP default ediffg is 10 x EDIFF
        ediff = settings.get("ediff", 1e-4)
        ediffg = settings.get("ediffg", ediff * 10)

        if ediffg == 0:
            # From the VASP wiki:
            # EDIFFG might be 0; in this case the ionic relaxation is stopped after NSW steps.
            return False
        if ediffg < 0:
            # Force criteria
            max_force = np.linalg.norm(last_results["forces"], axis=1).max()
            if max_force > -ediffg:
                return False
        if ediffg > 0:
            if len(atoms_history) < 2:
                # We cannot determine if we're converged
                return False
            energy_diff = last_results["energy"] - atoms_history[-2].calc.results["energy"]
            if energy_diff > ediffg:
                return False

        # Check if the stress tensor is OK
        # Only does cell optimization for isif >= 3
        isif = settings.get("isif", 0)
        print(isif)
        if isif >= 3:
            stress_ok = is_stress_converged(last_atoms, ediffg, isif)
            if not stress_ok:
                return False

    return True


def is_vasprun_converged(vasp_run) -> bool:
    return is_converged(vasp_run.atoms_history, vasp_run.run_settings)
