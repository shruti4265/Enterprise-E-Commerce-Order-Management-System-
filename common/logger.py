"""
logger.py
=========
Common logging module for the Enterprise E-Commerce Order Management System.

Every team member should import `get_logger` from this file instead of
creating their own logging configuration. This guarantees that all logs
(from Customer, Product, Inventory, Cart/Order, Payment, and Reports
modules) end up in the same format and the same log files, which makes
debugging a multi-module project far easier.

Usage
-----
    from common.logger import get_logger

    logger = get_logger(__name__)

    logger.info("Customer registered successfully")
    logger.warning("Stock running low for product_id=12")
    logger.error("Payment failed for order_id=45", exc_info=True)

Log files are written to a `logs/` folder (created automatically) and are
rotated daily so they don't grow indefinitely:
    logs/app.log       -> INFO and above (all normal activity)
    logs/error.log     -> ERROR and above only (for quick incident review)

Console output shows INFO and above by default, so nobody's terminal gets
flooded with DEBUG noise unless they explicitly turn it on.
"""

import logging
import os
from logging.handlers import TimedRotatingFileHandler

# ---------------------------------------------------------------------------
# Configuration constants (tweak here, once, for the whole project)
# ---------------------------------------------------------------------------
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
APP_LOG_FILE = os.path.join(LOG_DIR, "app.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Default levels — change to logging.DEBUG while actively debugging a module
CONSOLE_LEVEL = logging.INFO
FILE_LEVEL = logging.INFO
ERROR_FILE_LEVEL = logging.ERROR

_LOGGERS_CONFIGURED = set()


def _ensure_log_dir():
    """Create the logs/ directory if it doesn't already exist."""
    os.makedirs(LOG_DIR, exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger for the given module name.

    Every module in the project should call this once, near the top of
    the file, using __name__ so log lines show exactly where they came
    from:

        logger = get_logger(__name__)

    Parameters
    ----------
    name : str
        Usually __name__ of the calling module (e.g. "customer_management").

    Returns
    -------
    logging.Logger
        A logger with console + rotating file handlers attached.
    """
    logger = logging.getLogger(name)

    # Avoid attaching duplicate handlers if get_logger() is called more
    # than once for the same module (e.g. re-imports during testing).
    if name in _LOGGERS_CONFIGURED:
        return logger

    _ensure_log_dir()
    logger.setLevel(logging.DEBUG)  # capture everything; handlers filter it
    logger.propagate = False

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # --- Console handler: quick visibility while developing ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(CONSOLE_LEVEL)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # --- Rotating file handler: full activity log, rotates at midnight ---
    file_handler = TimedRotatingFileHandler(
        APP_LOG_FILE, when="midnight", backupCount=14, encoding="utf-8"
    )
    file_handler.setLevel(FILE_LEVEL)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # --- Error-only file handler: fast way to spot production issues ---
    error_handler = TimedRotatingFileHandler(
        ERROR_LOG_FILE, when="midnight", backupCount=30, encoding="utf-8"
    )
    error_handler.setLevel(ERROR_FILE_LEVEL)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    _LOGGERS_CONFIGURED.add(name)
    return logger


if __name__ == "__main__":
    # Quick self-test: run `python logger.py` to confirm log files are created.
    test_logger = get_logger("logger_selftest")
    test_logger.debug("This is a DEBUG message (file only, not console).")
    test_logger.info("Logger module initialized successfully.")
    test_logger.warning("This is a sample WARNING message.")
    try:
        1 / 0
    except ZeroDivisionError:
        test_logger.error("Sample ERROR with traceback:", exc_info=True)
    print(f"Check '{LOG_DIR}' for app.log and error.log")