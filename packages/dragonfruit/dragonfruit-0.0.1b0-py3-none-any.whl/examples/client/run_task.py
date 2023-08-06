import logging

import dragonfruit as df

logger = logging.getLogger(__name__)


def run(task_id):
    logger.info("Loading task %s", task_id)
    task = df.load(task_id)  # type: df.vasp.VaspTask
    logger.info("Running task %s", task_id)
    task.run()
    logger.info("Finished task %s", task_id)
