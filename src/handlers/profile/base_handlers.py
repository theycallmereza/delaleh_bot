from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from src.logging import LOGGER

logger = LOGGER("BaseProfileHandlers")


# Command: /cancel (to cancel the conversation)
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"User {update.message.from_user.id} canceled profile creation.")
    await update.message.reply_text("عملیات لغو شد.")
    return ConversationHandler.END
