from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters

from src.database import redis_store
from src.logging import LOGGER
from src.services.auth_service import AuthService

logger = LOGGER("DelalehBot")  # Logger instance for this file


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the /start command. Sends a welcome message with a contact button.
    """
    logger.info(f"User {update.message.from_user.id} started the bot.")
    contact_button = KeyboardButton("اشتراک گذاری شماره موبایل", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True)
    await update.message.reply_text("خوش اومدی برای ادامه شماره تلگرام خودت رو ارسال کن", reply_markup=keyboard)


async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the user's contact sharing. Authenticates the user and stores tokens in Redis.
    """
    contact = update.message.contact
    mobile_number = contact.phone_number
    telegram_id = str(update.message.from_user.id)
    username = update.effective_user.username or ""
    first_name = update.effective_user.first_name or ""
    last_name = update.effective_user.last_name or ""
    language_code = update.effective_user.language_code or ""

    logger.info(f"User {telegram_id} shared their contact: {mobile_number}")

    # Authenticate the user
    auth_service = AuthService(
        mobile_number=mobile_number,
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        language_code=language_code,
    )

    try:
        tokens = auth_service.login()
        logger.info(f"User {telegram_id} authenticated successfully.")

        # Store tokens in Redis
        redis_store.set_token(telegram_id, tokens["access"], tokens["refresh"])
        logger.info(f"Tokens stored in Redis for user {telegram_id}.")

        # Create a reply keyboard button for 'Complete Profile'
        profile_button = KeyboardButton("/create_profile")
        keyboard = ReplyKeyboardMarkup([[profile_button]], resize_keyboard=True)
        await update.message.reply_text("شمارت ثبت شد! برای ساختن پروفایل روی دکمه زیر بزن", reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Error authenticating user {telegram_id}: {e}")
        await update.message.reply_text("متاسفانه مشکلی پیش اومده. لطفا دوباره تلاش کن.")


def start_handlers(bot):
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(MessageHandler(filters.CONTACT, handle_contact))
