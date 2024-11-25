import logging


def set_log_level(level: str) -> None:
    """Set the logging level for the package."""
    logger = logging.getLogger("gensor")
    logger.setLevel(level.upper())
