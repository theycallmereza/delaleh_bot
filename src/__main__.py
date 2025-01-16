from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from src import bot
from src.handlers.authentication.start import handle_contact, start
from src.handlers.profile.create_profile import (
    STATES,
    cancel,
    create_profile,
    handle_bio,
    handle_birth_date,
    handle_height,
    handle_image,
    handle_location,
    handle_name,
)
from src.logging import LOGGER

# Initialize logger
logger = LOGGER(__name__)
logger.info("Client successfully initiated....")

# Add handlers
bot.add_handler(CommandHandler("start", start))
bot.add_handler(MessageHandler(filters.CONTACT, handle_contact))

# Conversation handler for /create_profile
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("create_profile", create_profile)],
    states={
        STATES.NAME.value: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)],
        STATES.BIRTH_DATE.value: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_birth_date)],
        STATES.BIO.value: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_bio)],
        STATES.HEIGHT.value: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_height)],
        STATES.IMAGE.value: [MessageHandler(filters.PHOTO | filters.TEXT, handle_image)],
        STATES.LOCATION.value: [MessageHandler(filters.LOCATION | filters.TEXT, handle_location)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
bot.add_handler(conv_handler)


# Error handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error: {context.error}")
    if update and hasattr(update, "message"):
        await update.message.reply_text("An error occurred. Please try again.")


bot.add_error_handler(error_handler)

if __name__ == "__main__":
    logger.info("Starting bot...")
    bot.run_polling()
