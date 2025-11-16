"""Simple logging configuration for the package."""

import logging


def setup_logging(level: str = "INFO", include_timestamp: bool = True) -> None:
    """Configure logging for the pyswap package.

    Call this function to enable logging output from pyswap. If not called,
    pyswap will be silent by default (recommended for library usage).

    Parameters:
        level (str): The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        include_timestamp (bool): Whether to include timestamps in log messages.

    Example:
        >>> import pyswap
        >>> pyswap.setup_logging(level="DEBUG")
    """
    logger = logging.getLogger("pyswap")
    logger.setLevel(getattr(logging, level.upper()))

    # Remove NullHandler and any existing handlers
    logger.handlers.clear()

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    if include_timestamp:
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S"
        )
    else:
        formatter = logging.Formatter("%(levelname)s: %(message)s")

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.propagate = False


def set_log_level(level: str) -> None:
    """Set the logging level for the package.

    Note: setup_logging() must be called first to configure handlers.

    Parameters:
        level (str): The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    logger = logging.getLogger("pyswap")
    logger.setLevel(getattr(logging, level.upper()))
