from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from src import bot, config
from src.database import redis_store
from src.logging import LOGGER
from src.services.auth_service import AuthService

logger = LOGGER("DelalehBot")  # Creating a logger instance for this file


@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    # Send a welcome message and ask for mobile number using a contact button
    contact_button = KeyboardButton("Share Contact", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True)

    await message.reply("Welcome! Please share your contact info to continue.", reply_markup=keyboard)


@bot.on_message(filters.contact)
async def handle_contact(client, message: Message):
    # Extract the contact's mobile number and telegram_id
    mobile_number = message.contact.phone_number
    telegram_id = str(message.from_user.id)
    username = str(message.from_user.username)

    # Authenticate the user using the AuthService
    auth_service = AuthService(
        api_key=config.SERVER_API_KEY,  # Replace with actual API key
        mobile_number=mobile_number,
        telegram_id=telegram_id,
        username=username,
    )

    try:
        tokens = auth_service.login()
        # On successful authentication, send the access token to the user
        redis_store.set_token(telegram_id, tokens["access"], tokens["refresh"])
        # Create an inline button for 'Complete Profile'
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Complete Profile", callback_data="complete_profile")]])
        await message.reply("Bot started successfully!", reply_markup=keyboard)
    except Exception as e:
        # If authentication fails, show the error message
        await message.reply(f"Error: {str(e)}")


# Handling button click
@bot.on_callback_query()
async def on_button_click(client, callback_query):
    if callback_query.data == "complete_profile":
        # Handle profile completion
        telegram_id = str(callback_query.from_user.id)
        access_token, refresh_token = redis_store.get_token(telegram_id)
        await callback_query.message.reply(f"Access: {access_token}\nRefresh: {refresh_token}")
