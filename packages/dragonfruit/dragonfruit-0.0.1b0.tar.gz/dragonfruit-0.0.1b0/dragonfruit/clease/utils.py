import tempfile


def clease_temporary_database():
    return tempfile.NamedTemporaryFile(suffix=".db")
