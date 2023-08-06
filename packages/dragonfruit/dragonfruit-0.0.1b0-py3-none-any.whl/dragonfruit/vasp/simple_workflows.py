import logging
import uuid

from dragonfruit import mince
from . import base
from . import vasp_errors

__all__ = ("SimpleVaspWorkflow",)

logger = logging.getLogger(__name__)


class SimpleVaspWorkflow(base.VaspTask):
    TYPE_ID = uuid.UUID("d29adce9-8f39-4024-9c29-27e3c09e2d9f")

    def __init__(self, initial_atoms, initial_settings, historian=None):
        super(SimpleVaspWorkflow, self).__init__(initial_atoms, initial_settings)
        self._historian = historian or mince.get_historian()

    def run(self):
        try:
            with self.running():

                current_run = self.get_last_run()
                if not current_run:
                    # Initial run
                    current_run = self.new_run()
                    self.do_run(current_run)

                try:
                    while not current_run.converged:
                        # Do a restart
                        current_run = self.create_restart()
                        logger.warning("Doing a restart: %s", current_run.description)
                        self.do_run(current_run)
                except vasp_errors.PermanentFailure as exc:
                    logger.error("There was a catastrophic failure, I'm out: %s", exc)
                    return
                else:
                    logger.info("Doing final singlepoint calculation")
                    singlepoint = self.new_run()
                    singlepoint.settings["ibrion"] = -1
                    singlepoint.settings["nsw"] = 0
                    self.do_run(singlepoint)

            self.set_result(self.get_last_run().results)
            logger.info("Task finished")
        finally:
            self.save(self)

    def create_restart(self):
        return self._restarter.create_restart(self)

    def do_run(self, vasp_run: base.VaspRun):
        if vasp_run is not self.get_last_run():
            self.runs.append(vasp_run)
            self.save()

        logger.info("Executing:\nSettings: %s\nAtoms: %s", self.settings, vasp_run.atoms)
        with vasp_run.running():
            vasp_run.run()
        # Save after each run
        self.save()

    def load_instance_state(self, saved_state, loader):
        super().load_instance_state(saved_state, loader)
        self._historian = loader.get_historian()


HISTORIAN_TYPES = (SimpleVaspWorkflow,)
