from src import bot
from src.handlers.authentication.start import start_handlers
from src.handlers.base.error_handler import error_handlers
from src.handlers.profile.create_profile import create_profile_handler
from src.handlers.profile.my_profile import my_profile_handlers
from src.logging import LOGGER

# Initialize logger
logger = LOGGER(__name__)
logger.info("Client successfully initiated....")

# auth handlers
logger.info("Adding start handlers...")
start_handlers(bot)

# profile handlers
logger.info("Adding create profile handlers...")
create_profile_handler(bot)

logger.info("Adding my profile handlers...")
my_profile_handlers(bot)

# base handlers
logger.info("Adding error handlers...")
error_handlers(bot)

if __name__ == "__main__":
    logger.info("Starting bot...")
    bot.run_polling()
