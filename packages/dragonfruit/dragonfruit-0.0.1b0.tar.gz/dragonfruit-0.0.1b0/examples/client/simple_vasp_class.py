import dragonfruit as df


def run(task_id):
    vasp_task = df.load(task_id)  # type: df.vasp.SimpleVaspTask
    vasp_task.run()
