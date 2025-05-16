import sys
import time
import logging
import threading

from io import BytesIO

from typing import List, Union, Optional
from logging.handlers import RotatingFileHandler


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


class BufferedRotatingFileHandler(RotatingFileHandler):
    """Buffered handler with double reset condition"""
    def __init__(
        self,
        filename: str,
        mode: str = 'a',
        maxBytes: int = 0,
        backupCount: int = 0,
        bufferSize: Optional[int] = None,
        flushInterval: Optional[float] = None,
        encoding: Optional[str] = None,
        delay: bool = False
    ):
        super().__init__(
            filename,
            mode,
            maxBytes,
            backupCount,
            encoding,
            delay
        )
        self.buffer = BytesIO()
        self.bufferSize = bufferSize
        self.flushInterval = flushInterval
        self.lastFlush = time.monotonic()
        self._lock = threading.Lock()

    def emit(self, record):
        with self._lock:
            try:
                msg = self.format(record)
                
                if self.buffer and self.bufferSize:
                    self.buffer.write(msg.encode(self.encoding))
                    self.buffer.write(b'\n')

                    current_time = time.monotonic()
                    buffer_full = self.buffer.tell() >= self.bufferSize
                    time_expired = (current_time - self.lastFlush) >= self.flushInterval

                    if buffer_full or time_expired:
                        self._flush_buffer()

                elif self.stream:
                    self.stream.write(msg)
                    self.stream.write('\n')
                    self.stream.flush()

                if self.shouldRollover(record):
                    self.doRollover()
            except Exception as e:
                self.handleError(record)

    def close(self):
        with self._lock:
            try:
                self._flush_buffer()

                if self.stream:
                    self.stream.close()
            finally:
                super().close()

    def _flush_buffer(self):
        if self.buffer.tell() > 0:
            self.stream.write(self.buffer.getvalue() \
                              .decode(self.encoding))
            self.stream.flush()
            self.buffer = BytesIO()
            self.lastFlush = time.monotonic()


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
        max_bytes: int = 48 * 1024 * 1024,
        backup_count: int = 5,
        buffer_size: Optional[int] = None,
        flush_interval: Optional[float] = None,
        encoding: str = "utf-8",
        ignored_loggers: List[str] = ["sqlalchemy", "sqlite3"]
    ):
        self._setup_logging(
            level,
            console_format,
            file_format,
            filename,
            max_bytes,
            backup_count,
            buffer_size,
            flush_interval,
            encoding,
            ignored_loggers
        )

    def _setup_logging(
        self,
        level: Union[str, int],
        console_format: str,
        file_format: str,
        filename: Optional[str],
        max_bytes: int,
        backup_count: int,
        buffer_size: Optional[int],
        flush_interval: Optional[float],
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
            file_handler = BufferedRotatingFileHandler(
                filename=filename,
                maxBytes=max_bytes,
                backupCount=backup_count,
                bufferSize=buffer_size,
                flushInterval=flush_interval,
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
