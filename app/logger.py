# Standard Imports
import logging

# Local Imports
from app.config import (
    LOGGER_INSTANCE_NAME, LOGGER_FILE_NAME, 
    LOGGER_LEVEL, LOGGER_LEVEL_CONSOLE, LOGGER_LEVEL_FILE, 
    LOGGER_FORMATTER
)

class CustomLogger:
    @staticmethod
    def get_logger(name: str = LOGGER_INSTANCE_NAME) -> logging.Logger:
        """
        Return a configured logger instance.
        If a logger with the given name already exists, it returns that instance.
        """
        logger = logging.getLogger(name)

        # Configure logger
        if not logger.hasHandlers():
            logger.setLevel(LOGGER_LEVEL)
            
            # File handler
            file_handler = logging.FileHandler(LOGGER_FILE_NAME)
            file_handler.setLevel(LOGGER_LEVEL_FILE)
            file_handler.setFormatter(LOGGER_FORMATTER)
            logger.addHandler(file_handler)
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(LOGGER_LEVEL_CONSOLE)
            console_handler.setFormatter(LOGGER_FORMATTER)
            logger.addHandler(console_handler)
            
        return logger
