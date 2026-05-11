"""
logger.py — Central Logging Configuration
Imported by all layers (database, schemas, crud, router) to ensure
consistent log formatting and output across the entire application.
"""

import logging
import sys
import os
from pathlib import Path

# Use environment variable for log file path, default to app.log in current directory
LOG_FILE = Path(os.getenv("LOG_FILE", Path(__file__).parent / "app.log"))

def get_logger(name: str) -> logging.Logger:
    """
    Returns a named logger with handlers attached (file + console).
    Call this once per module:  logger = get_logger(__name__)
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if get_logger is called multiple times
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler (INFO and above → app.log) 
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Console handler (DEBUG and above → stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
