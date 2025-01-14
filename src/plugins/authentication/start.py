from pyrogram import filters
from pyrogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from src import bot, config
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
        await message.reply(f"Logged in successfully! Your access token is: {tokens['access']}")
    except Exception as e:
        # If authentication fails, show the error message
        await message.reply(f"Error: {str(e)}")
