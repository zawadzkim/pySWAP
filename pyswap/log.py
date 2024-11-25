import logging


def set_log_level(level: str) -> None:
    """Set the logging level for the package."""
    logger = logging.getLogger("pyswap")
    logger.setLevel(level.upper())
