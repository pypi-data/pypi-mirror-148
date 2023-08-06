import logging

logger = logging.getLogger(__name__)

PROTECTED_KEYS = ("_directory", "name")

__all__ = ("sanitize_meta",)


def sanitize_meta(meta: dict) -> dict:
    """Sanitize a meta dictionary, and remove protected keywords"""
    new_meta = {}
    for key, value in meta.items():
        if key in PROTECTED_KEYS:
            logger.warning("Protected key %s found in meta dictionary, and is being removed", key)
        else:
            new_meta[key] = value
    return new_meta
