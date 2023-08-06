from ase.build import molecule

import minkipy

import dragonfruit as df

# pylint: disable=invalid-name

# Change the active project
minkipy.workon()

atoms = molecule("H2")
atoms.center(vacuum=5)
# atoms.pbc = True

vasp_task = df.vasp.VaspTask(
    atoms, dict(xc="LDA", encut=100, nelm=5, ibrion=2, ediffg=-1e-5, nsw=200)
)
restarter = vasp_task.get_restarter()
handlers = df.vasp.get_default_handlers()
restarter.register_many(handlers)
vasp_id = vasp_task.save()

# Create and submit the task
task = minkipy.task(
    "simple_vasp.py@run", args=(vasp_task,), folder="vasp_task_{}".format(str(vasp_id))
)
minkipy.queue().submit(task)
