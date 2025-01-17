"""Simple logging configuration for the package."""

import logging


def _setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)


def set_log_level(level: str) -> None:
    """Set the logging level for the package."""
    logger = logging.getLogger("pyswap")
    logger.setLevel(level.upper())
