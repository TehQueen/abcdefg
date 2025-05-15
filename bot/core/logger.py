import logging

from typing import Union


class LoggingSystem:
    BASE_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    """Comprehensive logging system with advanced features"""
    def __init__(
        self,
        level: Union[str, int] = "INFO",
        format: str = BASE_FORMAT
    ):
        self._setup_logging(
            level,
            format
        )

    def _setup_logging(
        self,
        level: Union[str, int],
        format: str
    ):
        # Basic Configuration Setup
        logging.basicConfig(
            level=level,
            format=format
        )

        # Checking the configuration
        logging.info("Logging system initialized with %s level", level)
