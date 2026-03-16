"""Logging configuration for mlpipe."""

from __future__ import annotations

from loguru import logger


def configure_logging(log_path: str = "logs/pipeline.log", level: str = "INFO") -> None:
    """Set up file-based logging with rotation.

    Call this explicitly when you want pipeline logs written to disk.
    Nothing happens at import time — the caller decides if/when to enable logging.

    Args:
        log_path: Destination file path.
        level: Minimum log level (DEBUG, INFO, WARNING, ERROR).
    """
    logger.add(log_path, rotation="1 MB", level=level)


__all__ = ["logger", "configure_logging"]
