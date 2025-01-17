from io import BytesIO

from khayyam import JalaliDate
from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from src.constant import STATES
from src.handlers.profile.base_handlers import cancel
from src.logging import LOGGER
from src.services.profile_service import ProfileService

logger = LOGGER("CreateProfileHandlers")  # Logger instance for this file


# Command: /create_profile
async def create_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"User {update.message.from_user.id} started profile creation.")
    await update.message.reply_text("اسمت:")
    return STATES.NAME.value


# Handle name input
async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text  # Store name
    logger.info(f"User {update.message.from_user.id} provided name: {update.message.text}")
    await update.message.reply_text(
        """
        تاریخ تولدت به صورت زیر وارد گن:
        1374-11-25
        """
    )
    return STATES.BIRTH_DATE.value  # Move to the BIRTH_DATE state


# Handle birth date input
async def handle_birth_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        birth_date = JalaliDate.strptime(update.message.text, "%Y-%m-%d")
        context.user_data["birth_date"] = birth_date.todate().strftime("%Y-%m-%d")  # Store birth date
        logger.info(f"User {update.message.from_user.id} provided birth date: {update.message.text}")
        await update.message.reply_text("قدت:")
        return STATES.HEIGHT.value  # Move to the HEIGHT state
    except ValueError:
        logger.warning(f"User {update.message.from_user.id} provided invalid birth date: {update.message.text}")
        await update.message.reply_text(
            """
            تاریخ تولدت به صورت زیر وارد گن:
            1374-11-25
            """
        )
        return STATES.BIRTH_DATE.value  # Stay in the BIRTH_DATE state


# Handle height input
async def handle_height(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        height = int(update.message.text)
        if height < 50 or height > 250:
            raise ValueError("Height out of range")
        context.user_data["height"] = height  # Store height
        logger.info(f"User {update.message.from_user.id} provided height: {update.message.text}")
        await update.message.reply_text("دربارع خودت یه چی بنویس:")
        return STATES.BIO.value  # Move to the BIO state
    except ValueError:
        logger.warning(f"User {update.message.from_user.id} provided invalid height: {update.message.text}")
        await update.message.reply_text("لطفا یک عدد معتبر بین 50 تا 250 وارد کن:")
        return STATES.HEIGHT.value  # Stay in the HEIGHT state


# Handle bio input
async def handle_bio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bio = update.message.text
    if len(bio) > 500:
        await update.message.reply_text("بیوگرافی باید کمتر از 500 کاراکتر باشه. لطفا کوتاه‌تر بنویس:")
        return STATES.BIO.value
    context.user_data["bio"] = bio  # Store bio
    logger.info(f"User {update.message.from_user.id} provided bio: {bio}")
    await update.message.reply_text("عکستو واسم بفرست:")
    return STATES.IMAGE.value  # Move to the IMAGE state


# Handle image input
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        # Get the highest resolution photo
        photo = update.message.photo[-1]
        file = await photo.get_file()

        # Download the image file
        image_data = BytesIO()
        await file.download_to_memory(out=image_data)
        image_data.seek(0)  # Reset the stream position

        # Store the image data in context.user_data
        context.user_data["image"] = image_data
        logger.info(f"User {update.message.from_user.id} uploaded an image.")

        await update.message.reply_text("موقعیت مکانیتو ارسال کن:")
        return STATES.LOCATION.value  # Move to the LOCATION state
    else:
        await update.message.reply_text("لطفا یک عکس ارسال کن:")
        return STATES.IMAGE.value  # Stay in the IMAGE state


# Handle location input
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.location:
        context.user_data["latitude"] = update.message.location.latitude  # Store latitude
        context.user_data["longitude"] = update.message.location.longitude  # Store longitude
        logger.info(f"User {update.message.from_user.id} shared their location.")
        return await show_profile(update, context)  # Show the profile
    else:
        await update.message.reply_text("لطفا موقعیت مکانیتو ارسال کن:")
        return STATES.LOCATION.value  # Stay in the LOCATION state


# Show the profile
async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    profile_service = ProfileService(telegram_id=update.message.from_user.id)

    # Prepare the profile data
    profile_data = context.user_data.copy()

    # If an image was uploaded, pass the file data
    if "image" in profile_data and profile_data["image"]:
        profile_data["image"] = profile_data["image"].getvalue()  # Convert BytesIO to bytes

    response = profile_service.update_profile(profile_data)
    logger.info(f"User {update.message.from_user.id} completed profile creation.")

    # Format the caption
    caption = (
        f"اسم: {response['name']}\n"
        f"سن: {response['age']}\n"
        f"قد: {response['height']} \n"
        f"شهر: {response['location']} \n"
        f"درباره من: {response['bio']}\n"
    )
    # Send the photo with the caption
    await update.message.reply_photo(
        photo=response["image"],
        caption=caption,
    )
    return ConversationHandler.END  # End the conversation


def create_profile_handler(bot):
    # Conversation handler for /create_profile
    create_profile_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("create_profile", create_profile)],
        states={
            STATES.NAME.value: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)],
            STATES.BIRTH_DATE.value: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_birth_date)],
            STATES.BIO.value: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_bio)],
            STATES.HEIGHT.value: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_height)],
            STATES.IMAGE.value: [MessageHandler(filters.PHOTO | filters.TEXT, handle_image)],
            STATES.LOCATION.value: [MessageHandler(filters.LOCATION | filters.TEXT, handle_location)],
        },
        fallbacks=[CommandHandler("cancel_create", cancel)],
    )
    bot.add_handler(create_profile_conv_handler)
