import logging
import os
from logging.handlers import RotatingFileHandler

# Constants
LOG_FILE = "logs.txt"
MAX_LOG_SIZE = 5_000_000  # 5 MB
BACKUP_COUNT = 3

# Remove old log file if it exists
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE, mode="w+", maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT),
        logging.StreamHandler(),
    ],
)

# Suppress INFO messages from external libraries
logging.getLogger("pyrogram").setLevel(logging.ERROR)


def LOGGER(name: str) -> logging.Logger:
    """
    Returns a logger instance with the given name.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: A configured logger instance.
    """
    return logging.getLogger(name)
