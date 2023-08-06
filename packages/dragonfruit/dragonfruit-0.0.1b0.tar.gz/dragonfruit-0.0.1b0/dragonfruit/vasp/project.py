import uuid

import mincepy
import mincepy.builtins

from dragonfruit import mince

__all__ = ("VaspProject",)


class VaspProject(mincepy.BaseSavableObject):
    ATTRS = "name", "tasks"
    TYPE_ID = uuid.UUID("6ecedecf-b108-4c3f-93ce-8f52c4527fdc")

    def __init__(self, name=""):
        super(VaspProject, self).__init__()
        self.name = name
        self.tasks = []

    @classmethod
    def get_or_create(cls, name, historian=None):
        historian = historian or mince.get_historian()
        results = list(historian.find(cls, state={"name": name}))
        if not results:
            return VaspProject(name)

        if len(results) > 1:
            raise ValueError(
                "Multiple projects with the name '{}' found: {}".format(
                    name, [historian.get_obj_id(project) for project in results]
                )
            )

        return results[0]


HISTORIAN_TYPES = (VaspProject,)
