import os

__all__ = ("is_slurm", "NotASlurmEnvironment")


class NotASlurmEnvironment(RuntimeError):
    """Error to denote that the environment is not a SLURM environment"""


def is_slurm() -> bool:
    return bool(os.environ.get("SLURM_JOB_ID", False))
