import mincepy

__all__ = "get_historian", "save", "load"


def get_historian():
    return mincepy.get_historian()


def load(*to_load):
    return get_historian().load(*to_load)


def save(*objs):
    return get_historian().save(*objs)
