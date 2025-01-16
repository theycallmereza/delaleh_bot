from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.ext import ContextTypes

from src import config
from src.database import redis_store
from src.logging import LOGGER
from src.services.auth_service import AuthService

logger = LOGGER("DelalehBot")  # Logger instance for this file


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send a welcome message with a contact button
    contact_button = KeyboardButton("اشتراک گذاری شماره موبایل", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True)
    await update.message.reply_text("خوش اومدی برای ادامه شماره تلگرام خودت رو ارسال کن", reply_markup=keyboard)


async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Extract contact's mobile number and Telegram ID
    contact = update.message.contact
    mobile_number = contact.phone_number
    telegram_id = str(update.message.from_user.id)
    username = update.effective_user.username or ""
    first_name = update.effective_user.first_name or ""
    last_name = update.effective_user.last_name or ""
    language_code = update.effective_user.language_code or ""

    # Authenticate the user
    auth_service = AuthService(
        api_key=config.SERVER_API_KEY,
        mobile_number=mobile_number,
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        language_code=language_code,
    )

    try:
        tokens = auth_service.login()
        # Store tokens in Redis
        redis_store.set_token(telegram_id, tokens["access"], tokens["refresh"])

        # Create an inline button for 'Complete Profile'
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("ساختن پروفایل", callback_data="complete_profile")]])
        await update.message.reply_text("شمارت ثبت شد! برای ساختن پروفایل روی دکمه زیر بزن", reply_markup=keyboard)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


async def on_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "complete_profile":
        # Handle profile completion
        telegram_id = str(query.from_user.id)
        access_token, refresh_token = redis_store.get_token(telegram_id)
        await query.message.reply_text(f"Access: {access_token}\nRefresh: {refresh_token}")
