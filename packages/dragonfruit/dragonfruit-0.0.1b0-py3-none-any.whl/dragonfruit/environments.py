import os
import re
import subprocess
from typing import Optional, Dict
import uuid

import mincepy
import mincepy.builtins

__all__ = "SLURM", "get_scheduler_environment", "SchedulerEnvironment"

SLURM = "slurm"


class SchedulerEnvironment(mincepy.BaseSavableObject):
    TYPE_ID = uuid.UUID("6d0b5788-ac75-4cb3-9ea3-996fa15bf8ca")
    ATTRS = ("_scheduler", "_stdout", "_stderr", "_extra")

    def __init__(self, scheduler, stdout, stderr, extra=None):
        super().__init__()
        self._scheduler = scheduler
        self._stdout = stdout
        self._stderr = stderr
        self._extra = extra

    @property
    def scheduler(self):
        return self._scheduler

    @property
    def stdout(self):
        return self._stdout

    @property
    def stderr(self):
        return self._stderr

    @property
    def extra(self):
        return self._extra


def get_scheduler_environment() -> Optional[SchedulerEnvironment]:
    environ = os.environ
    if "SLURM_JOB_NAME" in environ:
        try:
            return get_slurm_environment()
        except RuntimeError:
            pass

    return None


def get_slurm_environment() -> SchedulerEnvironment:
    environ = os.environ
    job_id = environ["SLURM_JOB_ID"]

    try:
        scontrol = subprocess.run(
            ["scontrol", "show", "job", job_id], stdout=subprocess.PIPE, check=True
        ).stdout.decode("utf-8")
    except subprocess.CalledProcessError as err:
        raise RuntimeError(err)

    job_settings = parse_slurm_job(scontrol)

    return parse_slurm_environment(job_settings)


def parse_slurm_environment(job_settings: Dict[str, str]) -> SchedulerEnvironment:
    """Parse a dictionary from the parse_slurm_job() function
    into a SchedulerEnvrionment class."""
    return SchedulerEnvironment(
        scheduler=SLURM,
        stdout=job_settings["StdOut"],
        stderr=job_settings["StdErr"],
        extra=job_settings,
    )


def parse_slurm_job(scontrol: str) -> Dict[str, str]:
    """Parse the output of a 'scontrol show job <jobid>' string into
    a dictionary. Splits on the first occurence of "=" on each line.
    Keys which contains a period are removed, as this causes issues with
    MongoDB.
    """
    options = {}
    for entry in re.split(r"\s+", scontrol):
        # Split on the first "="
        eqidx = entry.find("=")
        if eqidx != -1:
            key = entry[:eqidx]
            if "." not in key:
                # MongoDB is not OK with having dots in the key of a dictionary
                value = entry[eqidx + 1 :]
                options[key] = value
    return options


HISTORIAN_TYPES = (SchedulerEnvironment,)
