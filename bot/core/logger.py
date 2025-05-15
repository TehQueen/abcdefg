import sys
import time
import logging

from typing import List, Union, Optional


class ConsoleFormatter(logging.Formatter):
    """Formatter with colors for console"""
    COLORS = {
        logging.DEBUG: '\033[94m',
        logging.INFO: '\033[92m',
        logging.WARNING: '\033[93m',
        logging.ERROR: '\033[91m',
        logging.CRITICAL: '\033[91m'
    }
    RESET = '\033[0m'
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    def format(self, record):
        color = self.COLORS.get(record.levelno, '')
        formatter = logging.Formatter(
            f'{color}{self.FORMAT}{self.RESET}',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        return formatter.format(record)


class FileFormatter(logging.Formatter):
    """Minimalistic file formatter"""
    def format(self, record):
        return f"{time.time():.3f}|{record.levelname[:1]}|{record.name[:8]}|{record.msg}"


class LoggingSystem:
    CONSOLE_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    FILE_FORMAT = "%(message)s"

    """Comprehensive logging system with advanced features"""
    def __init__(
        self,
        level: Union[str, int] = "INFO",
        console_format: str = CONSOLE_FORMAT,
        file_format: str = FILE_FORMAT,
        filename: Optional[str] = None,
        encoding: str = "utf-8",
        ignored_loggers: List[str] = ["sqlalchemy", "sqlite3"]
    ):
        self._setup_logging(
            level,
            console_format,
            file_format,
            filename,
            encoding,
            ignored_loggers
        )

    def _setup_logging(
        self,
        level: Union[str, int],
        console_format: str,
        file_format: str,
        filename: Optional[str],
        encoding: str,
        ignored_loggers: List[str]
    ):
        # Setting up handlers
        handlers = []

        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ConsoleFormatter(console_format))
        handlers.append(console_handler)

        # File Handler
        if filename:
            file_handler = logging.FileHandler(
                filename=filename,
                encoding=encoding,
                delay=True,
            )
            file_handler.setFormatter(FileFormatter(file_format))
            handlers.append(file_handler)

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
