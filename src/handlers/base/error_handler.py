from telegram import Update
from telegram.ext import ContextTypes

from src.logging import LOGGER

logger = LOGGER("ErrorHandlers")


# Error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle errors in the bot.
    """
    logger.error(f"Update {update} caused error: {context.error}")

    # Check if the update has a message or a callback query
    if update.message:
        await update.message.reply_text("An error occurred. Please try again.")
    elif update.callback_query:
        await update.callback_query.answer("An error occurred. Please try again.")
    else:
        logger.error("Unable to send error message: No message or callback query in update.")


def error_handlers(bot):
    bot.add_error_handler(error_handler)
