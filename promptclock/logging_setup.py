# promptclock/logging_setup.py
from __future__ import annotations

import logging
import logging.handlers
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "promptclock.log"


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure root logger with console + rotating file handlers."""
    logger = logging.getLogger("promptclock")
    if logger.handlers:
        return logger  # already configured

    logger.setLevel(level)

    # Common format: timestamp | level | module:line | message
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(fmt)

    # Rotating file (up to ~1MB * 5 files)
    fh = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=1_000_000, backupCount=5, encoding="utf-8"
    )
    fh.setLevel(level)
    fh.setFormatter(fmt)

    logger.addHandler(ch)
    logger.addHandler(fh)
    logger.propagate = False
    logger.debug("Logger initialized")
    return logger
