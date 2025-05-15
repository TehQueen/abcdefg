import sys
import logging

from typing import List, Union


class LoggingSystem:
    CONSOLE_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    """Comprehensive logging system with advanced features"""
    def __init__(
        self,
        level: Union[str, int] = "INFO",
        console_format: str = CONSOLE_FORMAT,
        ignored_loggers: List[str] = ["sqlalchemy", "sqlite3"]
    ):
        self._setup_logging(
            level,
            console_format,
            ignored_loggers
        )

    def _setup_logging(
        self,
        level: Union[str, int],
        console_format: str,
        ignored_loggers: List[str]
    ):
        # Setting up handlers
        handlers = []

        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(console_format))
        handlers.append(console_handler)

        # Basic Configuration Setup
        logging.basicConfig(
            level=level,
            handlers=handlers,
            format=console_format,
            force=True,
        )

        # Optimizing logging performance
        logging._srcfile = None
        logging.logProcesses = False
        logging.logThreads = False
        logging.logMultiprocessing = False
        logging.raiseExceptions = False


        # Disabling unnecessary loggers
        for logger_name in ignored_loggers:
            logger = logging.getLogger(logger_name)
            logger.propagate = False
            logger.disabled = True

        # Checking the configuration
        logging.info("Logging system initialized with %s level", level)
