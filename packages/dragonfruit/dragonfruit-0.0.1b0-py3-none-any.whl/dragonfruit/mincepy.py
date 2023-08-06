from . import environments
from . import clease
from . import ionic_liquids
from . import vasp


def get_types():
    types = []
    types.extend(environments.HISTORIAN_TYPES)
    types.extend(clease.HISTORIAN_TYPES)
    types.extend(vasp.base.HISTORIAN_TYPES)
    types.extend(vasp.project.HISTORIAN_TYPES)
    types.extend(vasp.simple_workflows.HISTORIAN_TYPES)
    types.extend(vasp.vasp_default_errors.HISTORIAN_TYPES)
    types.extend(vasp.vasp_errors.HISTORIAN_TYPES)
    types.extend(vasp.workflows.workflows.HISTORIAN_TYPES)
    types.extend(vasp.workflows.legacy.HISTORIAN_TYPES)
    types.extend(clease.scripts.simple_vasp.HISTORIAN_TYPES)
    types.extend(ionic_liquids.MINCEPY_TYPES)

    return types
