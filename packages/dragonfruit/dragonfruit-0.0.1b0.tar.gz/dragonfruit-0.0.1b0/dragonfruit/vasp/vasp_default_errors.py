"""Module for handling VASP errors and autmating possible fixes.

Credit to Felix for several of these.
"""

from typing import Optional, Sequence, Tuple
from uuid import UUID

from dragonfruit import utils
from . import base
from . import vasp_errors
from .vasp_errors import ErrorHandler

__all__ = (
    "get_default_handlers",
    "SlurmTimedOut",
    "SimpleAdjustment",
    "NotHermitian",
    "Invgrp",
    "Rhosyg",
    "Zbrent",
    "ZbrentAlternative",
    "Posmap",
    "Fexcp",
    "Pzstein",
    "Sgrcon",
    "MaxRestarts",
    "WavecarUnusable",
    "PssyevxParallelization",
    "Pssyevx",
)


def restart_description(name):
    return f"restart after handling error {name}"


class SlurmTimedOut(ErrorHandler):
    """Handle cases where slurm killed the job because it exceeded the allowed time"""

    TYPE_ID = UUID("db59fe0c-460d-4c46-aa39-ea4ea97c565c")
    NAME = "slurm-timed-out"

    def __call__(self, vasp_task: base.VaspTask):
        err_str = "DUE TO TIME LIMIT"

        last_run = vasp_task.get_last_run()
        scheduler_env = last_run.scheduler_env
        if scheduler_env and utils.is_string_in_file(scheduler_env.stderr, err_str):
            # Ask the last run to update itself from the state of the files.
            # Also mark this run as completed, since we will be resuming on a new run.
            last_run.update_and_set_results()

            # Restart logic for a timed out job
            restart = last_run.create_restart(
                init_kwargs={"description": restart_description(self.NAME)}
            )
            vasp_task.runs.append(restart)
            return restart

        return self.SKIP


def is_simple_adjustment_possible(vasp_task, err_str) -> bool:
    """Check if a simple adjustment is possible.
    Basically checks if a error string is present in the stdout of a vasp task.
    """
    last_run = vasp_task.get_last_run()
    stdout = last_run.vasp_stdout
    return stdout and utils.is_string_in_file(last_run.vasp_stdout, err_str)


class SimpleAdjustment(ErrorHandler):
    ADJUSTMENT = None
    ERROR_STRING = None
    NAME = None
    TEMPORARY = False

    def __call__(self, vasp_task: base.VaspTask) -> Optional[base.VaspRun]:
        adj = self.ADJUSTMENT
        last_run = vasp_task.get_last_run()
        restart = None
        if not is_simple_adjustment_possible(vasp_task, self.ERROR_STRING):
            # This task cannot deal with it
            return self.SKIP

        # Check if the settings we want to apply are already there
        last_settings = last_run.run_settings
        if all(value == last_settings.get(key, None) for key, value in adj.items()):
            # We cannot fix it - we are already running on these settings
            # Note: Some adjustments rely on this behavior, if they have multiple
            # steps they want to check
            return self.SKIP

        restart = last_run.create_restart(
            init_kwargs={"description": restart_description(self.NAME)}
        )
        if self.TEMPORARY:
            restart.settings_overwrites.update(adj)
        else:
            restart.settings.update(adj)

        return restart


class NotHermitian(SimpleAdjustment):
    """Handles a single error"""

    TYPE_ID = UUID("e7a5acb2-08b8-41cd-b5d1-b49c2caa25c7")
    NAME = "not-hermitian"
    ADJUSTMENT = {"prec": "accurate"}
    ERROR_STRING = "WARNING: Sub-Space-Matrix is not hermitian in DAV"


class NotHermitianAlternative(SimpleAdjustment):
    """Alternate approach to not hermition, try changing the algorithm"""

    TYPE_ID = UUID("15bc1a2f-e9dd-4edf-92ba-5000cb3fdf1f")
    NAME = "not-hermitian-alternative"
    ADJUSTMENT = {"algo": "cg"}
    ERROR_STRING = "WARNING: Sub-Space-Matrix is not hermitian in DAV"


class Invgrp(SimpleAdjustment):
    """Handles a single error"""

    TYPE_ID = UUID("86ba6293-8f07-4207-a834-ca43315f227e")
    NAME = "invgrp"
    ADJUSTMENT = {"symprec": 1e-8}
    ERROR_STRING = "inverse of rotation matrix was not found (increase SYMPREC)"


class Rhosyg(SimpleAdjustment):
    TYPE_ID = UUID("25b9f6d4-f213-43b8-abb4-d018a0ab86a8")
    NAME = "rhosyg"
    ADJUSTMENT = {"symprec": 1e-4, "isym": 0}
    ERROR_STRING = "RHOSYG internal error: stars are not distinct"


class Zbrent(SimpleAdjustment):
    TYPE_ID = UUID("ed5edfad-3924-404e-8914-7ff9a970b5d9")
    NAME = "zbrent"
    ADJUSTMENT = {"algo": "all", "ediff": 1e-6}
    ERROR_STRING = "ZBRENT: fatal error"


class ZbrentAlternative(ErrorHandler):
    """Zbrent error can cause VASP to have the last atoms object be
    the same as the first.
    Instead, we use the second-to-last atoms object.

    We use a max count, to prevent any possible deadlocks, so we cannot get stuck
    in this error handler.
    """

    TYPE_ID = UUID("5c79a739-a052-4455-86f9-f69fe207c7bd")
    NAME = "zbrent_alternative"
    ERROR_STRING = "ZBRENT: fatal error"
    ATTRS = ("count", "max_count")

    # Default fall-back variables, for backwards compatbility
    # due to bug, see !81
    count = 0
    max_count = 3

    def __init__(self, max_count=3):
        super().__init__()
        self.count = 0
        self.max_count = max_count

    def __call__(self, vasp_task: base.VaspTask) -> Optional[base.VaspRun]:
        if not is_simple_adjustment_possible(vasp_task, self.ERROR_STRING):
            # We cannot deal with it here
            return self.SKIP

        if self.count >= self.max_count:
            # We used this restarter too many times, may be looping
            return self.SKIP

        last_run = vasp_task.get_last_run()
        atoms_history = last_run.atoms_history
        if len(atoms_history) < 2:
            # We didn't do enough, we'd just be running the same atoms again
            return self.SKIP

        penultimate_atoms = atoms_history[-2]
        # Use the second to last atoms object instead.
        restart = last_run.create_restart(
            init_kwargs={"description": restart_description(self.NAME)}, atoms=penultimate_atoms
        )
        self.count += 1
        return restart


class Posmap(SimpleAdjustment):
    TYPE_ID = UUID("22bad6b1-6d9a-4790-bc05-7ff2cd201f35")
    NAME = "posmap"
    ADJUSTMENT = {"symprec": 1e-8}
    ERROR_STRING = "POSMAP internal error: symmetry equivalent atom not found"


class Fexcp(SimpleAdjustment):
    TYPE_ID = UUID("e8ff0772-2727-44a0-858a-efaad5990367")
    NAME = "fexcp"
    ADJUSTMENT = {"algo": "all"}
    ERROR_STRING = "ERROR FEXCP: supplied Exchange"


class Pzstein(SimpleAdjustment):
    TYPE_ID = UUID("1de05f4e-7ff9-41c3-b4b0-68a9e09be7cc")
    NAME = "pzstein"
    ADJUSTMENT = {"algo": "all"}
    ERROR_STRING = "PZSTEIN parameter number"


class Sgrcon(SimpleAdjustment):
    TYPE_ID = UUID("c3ee2a32-6c51-4685-9f2b-6e979c4c4e8d")
    NAME = "sgrcon"
    # isym=0 might already lead to convergence
    # symprec and ediff just added for robustness
    ADJUSTMENT = {"isym": 0, "symprec": 1e-8, "ediff": 1e-7}
    ERROR_STRING = "internal error in subroutine SGRCON"


class WavecarUnusable(SimpleAdjustment):
    """If the wavecar is unusable from the previous run then temporarily disable it's use for the
    next run only"""

    TYPE_ID = UUID("ba1a5e64-b140-4fe3-9920-a2b7a5f11d33")
    NAME = "wavecar_sucks"
    TEMPORARY = True
    ADJUSTMENT = {"istart": 0}
    ERROR_STRING = "ERROR: while reading WAVECAR, plane wave coefficients changed"


class Pssyevx(SimpleAdjustment):
    """Handles a single error"""

    TYPE_ID = UUID("cf961d8f-eac1-4215-9a0f-3ea8ff95e525")
    NAME = "pssyevx"
    ADJUSTMENT = {"algo": "normal"}
    ERROR_STRING = "ERROR in subspace rotation PSSYEVX"


class PssyevxParallelization(SimpleAdjustment):
    """Alternate fix for PSSYEVX error, in case it's a parallelization issue"""

    TYPE_ID = UUID("b18d9736-a864-4e93-beb1-7bb272932ae9")
    NAME = "pssyevx-parallelization"
    # Disable npar, use simplest parallelization
    ADJUSTMENT = {"ncore": 1, "npar": None}
    ERROR_STRING = "ERROR in subspace rotation PSSYEVX"


class Pricel(SimpleAdjustment):
    ERROR_STRING = "internal error in subroutine PRICEL"
    NAME = "pricel"
    ADJUSTMENT = {"isym": 0}
    TYPE_ID = UUID("bf9fdfe8-ff87-4f4a-bf27-e324fe498d7e")


class MaxRestarts(ErrorHandler):
    """If no one else deals with the error then this handler attempts a simple restart changing no
    settings. If this happens more than max_count times in a task then it will order a termination.
    """

    TYPE_ID = UUID("108aee5f-a67e-4648-91bf-a65f6f56fcca")
    NAME = "max-restarts"
    ATTRS = ("count", "max_count", "raises")

    # Default fall-back variables, for backwards compatbility
    raises = True

    def __init__(self, max_count=3, raises=True):
        super().__init__()
        self.count = 0
        self.max_count = max_count
        self.raises = raises  # Should this error handler raise an error?

    def __call__(self, vasp_task: base.VaspTask) -> Optional[base.VaspRun]:
        if self.count < self.max_count:
            last_run = vasp_task.get_last_run()
            self.count += 1
            restart = last_run.create_restart(
                init_kwargs={"description": "Restart {} of {}".format(self.count, self.max_count)}
            )
            return restart

        if self.raises:
            raise vasp_errors.PermanentFailure(
                "Can't restart fool, reached '{}' attempts".format(self.max_count)
            )
        return self.SKIP


def get_default_handlers() -> Sequence[Tuple[ErrorHandler, int]]:
    return (
        (MaxRestarts(), 10),
        (NotHermitianAlternative(), 15),
        (NotHermitian(), 20),
        (Invgrp(), 30),
        (Rhosyg(), 40),
        (ZbrentAlternative(), 45),
        (Zbrent(), 50),
        (Posmap(), 60),
        (Pricel(), 65),
        (PssyevxParallelization(), 70),
        (Pssyevx(), 80),  # First we do one, then the other
        (Fexcp(), 90),
        (Pzstein(), 100),
        (Sgrcon(), 110),
        (WavecarUnusable(), 120),
        (SlurmTimedOut(), 130),
    )


HISTORIAN_TYPES = (
    SlurmTimedOut,
    NotHermitian,
    Invgrp,
    Rhosyg,
    Zbrent,
    Posmap,
    Fexcp,
    Pzstein,
    Sgrcon,
    MaxRestarts,
    WavecarUnusable,
    PssyevxParallelization,
    Pssyevx,
    Pricel,
    ZbrentAlternative,
    NotHermitianAlternative,
)
