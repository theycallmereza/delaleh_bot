import asyncio
import sys
import time

from telegram.ext import Application

from src import config
from src.logging import LOGGER

# Initialize logger
logger = LOGGER(__name__)


def check_python_version():
    """Check if the Python version is 3.7 or above."""
    if sys.version_info < (3, 7):
        logger.critical(
            """
=============================================================
You MUST need to be on Python 3.7 or above, shutting down the bot...
=============================================================
"""
        )
        sys.exit(1)


def setup_event_loop():
    """Set up the asyncio event loop."""
    logger.info("Setting up event loop...")
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop


def print_banner():
    """Print the bot banner."""
    logger.info(
        r"""
  ___      _      _     _    ___      _
 |   \ ___| |__ _| |___| |_ | _ ) ___| |_
 | |) / -_) / _` | / -_) ' \| _ \/ _ \  _|
 |___/\___|_\__,_|_\___|_||_|___/\___/\__|
"""
    )


def initialize_bot():
    """Initialize the Telegram bot."""
    logger.info("Initiating the client...")
    return Application.builder().token(config.BOT_TOKEN).build()


# Main initialization logic
logger.info("Starting DelalehBot...")
BotStartTime = time.time()

# Check Python version
check_python_version()

# Set up event loop
loop = setup_event_loop()

# Print bot banner
print_banner()

# Initialize the bot
bot = initialize_bot()
