from pathlib import Path
import shlex
import subprocess
import os
import warnings
from typing import Union, Sequence

from . import utils

__all__ = ("py_to_sh", "create_command", "submit_script", "dependency", "self_dependency")

ALLOWED_AFTER = ("after", "afterany", "afternotok", "afterok")


def _prolog():
    """Prolog function, which prints some useful information
    in the beginning of the bash function"""
    envvars = {
        "User": "SLURM_JOB_USER",
        "Job Name": "SLURM_JOB_NAME",
        "Start Time": "DATE",
        "Job ID": "SLURM_JOB_ID",
        "Partition": "SLURM_JOB_PARTITION",
        "Node List": "SLURM_JOB_NODELIST",
    }

    parts = []
    dashes = 16
    intro_string = f'{dashes*"-"} PROLOG {dashes*"-"}'

    parts.append(intro_string)
    for key, val in envvars.items():
        key += ":"
        sub_string = f"{(key):<15s} ${val}"
        parts.append(sub_string)
    parts.append(len(intro_string) * "-")

    # Export date variable
    script = 'DATE=`date +"%T %a %d-%m-%Y"`\n'
    for part in parts:
        script += f'echo "{part}"\n'

    return script


def py_to_sh(filename: Union[str, Path], script_args: Sequence[str] = None) -> str:
    """Convert a python file into a shell file for a SLURM submission.
    The same python file will be used for a python execution.
    Will add the prolog to the shell script.
    Returns the script as a string.

    :param filename: Filename of the python file. Should end in ".py"
    :param script_args: List of arguments to be passed along with the python file, in a
        "python <filename> <arg_1> <arg_2> ... <arg_N>" format.
    """
    filename = Path(filename)

    if filename.suffix != ".py":
        raise ValueError(f"File should be a python file, but got {filename}")

    # Build a new script
    script = "#!/usr/bin/env sh\n"

    with filename.open("r") as file:
        for line in file:
            if line.startswith("#SBATCH"):
                script += line

    script += _prolog()

    # Make python execution line
    py_exec = f"python {filename}"
    if script_args:
        script_args = " ".join(script_args)
        py_exec += f" {script_args}"
    py_exec += "\n"

    script += py_exec

    script += "errcode=$?\n"  # Capture script errorcode
    script += "exit $errcode\n"  # Remember to return correct errorcode
    return script


def dependency(job_id: int, after: str = "afterany"):
    """Create SLURM dependency string.

    :param job_id: SLURM id of the job to depend on
    :param after: Type of dependency. Default: 'afterany'
    """
    after = after.lower()
    if after not in ALLOWED_AFTER:
        msg = f"Expected an after value in {ALLOWED_AFTER}, but got {after}"
        raise ValueError(msg)
    return f"--dependency={after}:{job_id}"


def self_dependency(after: str = "afterany"):
    """Create SLURM dependency string on the job itself.
    Requires that it is called from within a SLURM environment

    :param after: Type of dependency. Default: 'afterany'
    """

    if not utils.is_slurm():
        msg = "Job does not look like a slurm environment."
        raise utils.NotASlurmEnvironment(msg)

    job_id = os.environ["SLURM_JOB_ID"]
    return dependency(job_id, after=after)


def create_command(sbatch_args: str = None, depend_self=False, after="afterany") -> Sequence[str]:
    """Create a command for SLURM submission, to be used with the "submit_script" function.

    :param sbatch_args: Single string containing the SLURM options, including the flags,
        e.g. sbatch_args='-N 1 -n 40 -p xeon40'
    :param depend_self: Bool, add a dependency on the calling job.
        Requires that it is called from within a SLURM environment (otherwise, a warning is raised)
        Default: False
    :param after: Type of dependency, only relevant is depend_self is True.
        Default: 'afterany'.
    """
    cmd = ["sbatch"]
    if sbatch_args:
        cmd += shlex.split(sbatch_args)

    if depend_self:
        try:
            cmd += [self_dependency(after=after)]
        except utils.NotASlurmEnvironment:
            msg = (
                "Job does not look like a slurm environment. " "Continuing without self dependency."
            )
            warnings.warn(msg)

    return cmd


def submit_script(script: str, command: Sequence[str]):
    """Submit submit script using a specified command."""
    subprocess.Popen(command, stdin=subprocess.PIPE).communicate(script.encode())
