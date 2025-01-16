from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, filters

from src import bot
from src.handlers.authentication.start import handle_contact, on_button_click, start
from src.logging import LOGGER

LOGGER(__name__).info("client successfully initiated....")
bot.add_handler(CommandHandler("start", start))
bot.add_handler(MessageHandler(filters.CONTACT, handle_contact))
bot.add_handler(CallbackQueryHandler(on_button_click))

if __name__ == "__main__":
    bot.run_polling()
