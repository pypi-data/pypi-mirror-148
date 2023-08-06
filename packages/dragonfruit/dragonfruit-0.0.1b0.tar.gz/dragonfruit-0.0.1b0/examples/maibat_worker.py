# pylint: disable=invalid-name
import sys
from pathlib import Path

import minkipy

import dragonfruit.slurm as ms

# SBATCH -N 1                            # Number of nodes
# SBATCH --ntasks-per-node=40            # Number of cores per node
# SBATCH -p xeon40                       # Pertition name
# SBATCH -t 2-02:00:00                   # Time
# SBATCH --mail-type=END,FAIL            # Send an e-mail on completion of any kind
# SBATCH --mail-user=<your-email>        # E-mail for SLURM logs

args = sys.argv[1:]

# Use the sys.argv to specify a job tag
tag = None
if args:
    tag = args[0]

slurm = ms.is_slurm()  # Are we in a SLURM environment?

# Input Settings #################################
project_name = None  # Project name
queues = ["xeon40-high", None]  # None is default queue

script = Path(sys.argv[0]).name  # Name of the script
jobname = "dragonfruit_worker"
if tag:
    jobname += f"_{tag}"

sbatch_args = f"-J {jobname}"
script_args = args  # Transfer the sys.argv arguments to the script
depend_self = True  # Should we add a self dependency?

timeout = 30.0  # Timeout for worker to wait for a job
max_tasks = -1  # Number of jobs to run in queue
##################################################

if not slurm:
    # Cannot depend on self if we're not in SLURM
    depend_self = False

script = ms.py_to_sh(script, script_args=script_args)
command = ms.create_command(sbatch_args=sbatch_args, depend_self=depend_self)

project = minkipy.workon(project_name)

# Only submit if we have jobs left in queue
do_submit = sum(minkipy.queue(queue).size() for queue in queues) > 0

if do_submit:
    command_string = " ".join(command)  # Command "stringified"
    print(f"Submitting job with the following command: {command_string}")
    ms.submit_script(script, command)

if slurm:
    # We only run if we're inside of a slurm environmnet
    for queue_name in queues:
        print(f"Running in queue {queue_name}")
        queue = minkipy.queue(queue_name)
        n_jobs = minkipy.workers.run(queue, max_tasks=max_tasks, timeout=timeout)
        print(f"Ran {n_jobs} jobs.")
