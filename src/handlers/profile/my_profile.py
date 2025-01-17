from io import BytesIO

from khayyam import JalaliDate
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from src.constant import UpdateProfileStates
from src.logging import LOGGER
from src.services.profile_service import ProfileService

logger = LOGGER("MyProfileHandlers")  # Logger instance for this file


async def my_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /my_profile command.
    """
    try:
        logger.info(f"User {update.message.from_user.id} called /my_profile.")  # Log the command
        # Fetch the user's profile data
        telegram_id = update.message.from_user.id
        profile_service = ProfileService(telegram_id=telegram_id)
        profile_data = profile_service.get_profile()

        # Format the caption
        caption = (
            f"اسم: {profile_data['name']}\n"
            f"سن: {profile_data['age']}\n"
            f"قد: {profile_data['height']} \n"
            f"شهر: {profile_data['location']} \n"
            f"درباره من:\n {profile_data['bio']}\n"
        )

        # Create an inline keyboard with buttons for updating fields
        keyboard = [
            [InlineKeyboardButton("ویرایش اسم", callback_data="update_name")],
            [InlineKeyboardButton("ویرایش تاریخ تولد", callback_data="update_birth_date")],
            [InlineKeyboardButton("ویرایش درباره من", callback_data="update_bio")],
            [InlineKeyboardButton("ویرایش قد", callback_data="update_height")],
            [InlineKeyboardButton("ویرایش عکس", callback_data="update_image")],
            [InlineKeyboardButton("ویرایش شهر", callback_data="update_location")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send the profile photo with the caption and buttons
        await update.message.reply_photo(
            photo=profile_data["image"],
            caption=caption,
            reply_markup=reply_markup,
        )
        logger.info(f"Profile data sent to user {update.message.from_user.id}.")  # Log successful response
    except Exception as e:
        logger.error(f"Error in my_profile for user {update.message.from_user.id}: {e}")  # Log the error
        await update.message.reply_text("خطایی رخ داد. لطفا دوباره تلاش کنید.")


async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle button clicks from the inline keyboard.
    """
    query = update.callback_query
    await query.answer()

    try:
        action = query.data
        logger.info(f"User {query.from_user.id} clicked button: {action}")  # Log the button click

        # Check if query.message exists before accessing it
        if not query.message:
            logger.error(f"User {query.from_user.id} clicked button, but no message found.")
            return

        if action == "update_name":
            await query.message.reply_text("اسم جدیدت رو وارد کن:")
            logger.info(f"Transitioning to state: {UpdateProfileStates.NAME.value}")
            return UpdateProfileStates.NAME.value
        elif action == "update_birth_date":
            await query.message.reply_text("سن جدیدت رو وارد کن:")
            logger.info(f"Transitioning to state: {UpdateProfileStates.BIO.value}")
            return UpdateProfileStates.BIRTH_DATE.value
        elif action == "update_bio":
            await query.message.reply_text("درباره من جدیدت رو وارد کن:")
            logger.info(f"Transitioning to state: {UpdateProfileStates.BIO.value}")
            return UpdateProfileStates.BIO.value
        elif action == "update_height":
            await query.message.reply_text("قد جدیدت رو وارد کن (به سانتی‌متر):")
            logger.info(f"Transitioning to state: {UpdateProfileStates.HEIGHT.value}")
            return UpdateProfileStates.HEIGHT.value
        elif action == "update_image":
            await query.message.reply_text("عکس پروفایل جدیدت رو ارسال کن:")
            logger.info(f"Transitioning to state: {UpdateProfileStates.IMAGE.value}")
            return UpdateProfileStates.IMAGE.value
        elif action == "update_location":
            await query.message.reply_text("موقعیت مکانیتو با تلگرام ارسال کن:")
            logger.info(f"Transitioning to state: {UpdateProfileStates.LOCATION.value}")
            return UpdateProfileStates.LOCATION.value
    except Exception as e:
        logger.error(f"Error in handle_button_click for user {query.from_user.id}: {e}")  # Log the error
        if query.message:
            await query.message.reply_text("خطایی رخ داد. لطفا دوباره تلاش کنید.")
        else:
            logger.warning("No message to reply to in case of error.")


async def update_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the new name input.
    """
    try:
        new_name = update.message.text
        telegram_id = update.message.from_user.id
        logger.info(f"User {telegram_id} submitted new name: {new_name}")  # Log the new name

        # Update the name in the database or API
        profile_service = ProfileService(telegram_id=telegram_id)
        profile_service.update_profile({"name": new_name})

        await update.message.reply_text("اسمت اپدیت شد!")
        logger.info(f"Name updated for user {telegram_id}.")  # Log successful update
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Error in update_name for user {update.message.from_user.id}: {e}")  # Log the error
        await update.message.reply_text("خطایی در اپدیت اسم رخ داد. لطفا دوباره تلاش کنید.")
        return UpdateProfileStates.NAME.value


async def update_birth_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        telegram_id = update.message.from_user.id
        new_birth_date = update.message.text
        logger.info(f"User {telegram_id} submitted new name: {new_birth_date}")  # Log the new name
        new_birth_date = JalaliDate.strptime(new_birth_date, "%Y-%m-%d")
        new_birth_date = new_birth_date.todate().strftime("%Y-%m-%d")  # Store birth date

        # Update the name in the database or API
        profile_service = ProfileService(telegram_id=telegram_id)
        profile_service.update_profile({"birth_date": new_birth_date})

        await update.message.reply_text("سنت اپدیت شد!")
        logger.info(f"Age updated for user {telegram_id}.")  # Log successful update
        return ConversationHandler.END
    except ValueError:
        logger.warning(f"User {update.message.from_user.id} provided invalid birth date: {update.message.text}")
        await update.message.reply_text(
            """
            تاریخ تولدت به صورت زیر وارد گن:
            1374-11-25
            """
        )
        return UpdateProfileStates.BIRTH_DATE.value  # Stay in the BIRTH_DATE state


async def update_bio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the new bio input.
    """
    try:
        new_bio = update.message.text
        telegram_id = update.message.from_user.id
        logger.info(f"User {telegram_id} submitted new bio: {new_bio}")  # Log the new bio

        # Update the bio in the database or API
        profile_service = ProfileService(telegram_id=telegram_id)
        profile_service.update_profile({"bio": new_bio})

        await update.message.reply_text("درباره من اپدیت شد!")
        logger.info(f"Bio updated for user {telegram_id}.")  # Log successful update
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Error in update_bio for user {update.message.from_user.id}: {e}")  # Log the error
        await update.message.reply_text("خطایی در اپدیت درباره من رخ داد. لطفا دوباره تلاش کنید.")
        return UpdateProfileStates.BIO.value


async def update_height(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the new height input.
    """
    try:
        new_height = update.message.text
        telegram_id = update.message.from_user.id
        logger.info(f"User {telegram_id} submitted new height: {new_height}")  # Log the new height

        if not new_height.isdigit():
            await update.message.reply_text("لطفا یک عدد معتبر برای قد وارد کنید.")
            return UpdateProfileStates.HEIGHT.value

        # Update the height in the database or API
        profile_service = ProfileService(telegram_id=telegram_id)
        profile_service.update_profile({"height": int(new_height)})

        await update.message.reply_text("قد اپدیت شد!")
        logger.info(f"Height updated for user {telegram_id}.")  # Log successful update
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Error in update_height for user {update.message.from_user.id}: {e}")  # Log the error
        await update.message.reply_text("خطایی در اپدیت قد رخ داد. لطفا دوباره تلاش کنید.")
        return UpdateProfileStates.HEIGHT.value


async def update_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the new image input.
    """
    try:
        if update.message.photo:
            # Get the highest resolution photo
            photo = update.message.photo[-1]
            telegram_id = update.message.from_user.id
            file = await photo.get_file()

            # Download the image file
            image_data = BytesIO()
            await file.download_to_memory(out=image_data)
            image_data.seek(0)  # Reset the stream position

            # Update in the database or API
            profile_service = ProfileService(telegram_id=telegram_id)
            profile_service.update_profile({"image": image_data.getvalue()})

            logger.info(f"User {telegram_id} uploaded an image.")  # Log the image upload
            await update.message.reply_text("عکس اپدیت شد!")
            return ConversationHandler.END
        else:
            await update.message.reply_text("لطفا یک عکس ارسال کن:")
            return UpdateProfileStates.IMAGE.value
    except Exception as e:
        logger.error(f"Error in update_image for user {update.message.from_user.id}: {e}")  # Log the error
        await update.message.reply_text("خطایی در اپدیت عکس رخ داد. لطفا دوباره تلاش کنید.")
        return UpdateProfileStates.IMAGE.value


async def update_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the new location input.
    """
    try:
        if update.message.location:
            telegram_id = update.message.from_user.id
            latitude = update.message.location.latitude  # Store latitude
            longitude = update.message.location.longitude  # Store longitude
            logger.info(f"User {telegram_id} submitted new location: {latitude}, {longitude}")  # Log the new location

            # Update in the database or API
            profile_service = ProfileService(telegram_id=telegram_id)
            profile_service.update_profile({"latitude": latitude, "longitude": longitude})

            await update.message.reply_text("موقعیت مکانی اپدیت شد!")
            logger.info(f"Location updated for user {telegram_id}.")  # Log successful update
            return ConversationHandler.END
        else:
            await update.message.reply_text("لطفا موقعیت مکانیتو ارسال کن:")
            return UpdateProfileStates.LOCATION.value
    except Exception as e:
        logger.error(f"Error in update_location for user {update.message.from_user.id}: {e}")  # Log the error
        await update.message.reply_text("خطایی در اپدیت موقعیت مکانی رخ داد. لطفا دوباره تلاش کنید.")
        return UpdateProfileStates.LOCATION.value


async def cancel_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the cancel update command.
    """
    try:
        telegram_id = update.message.from_user.id
        logger.info(f"User {telegram_id} canceled the profile update.")  # Log the cancel action

        # Send a confirmation message to the user
        await update.message.reply_text("عملیات آپدیت پروفایل لغو شد.")

        return ConversationHandler.END  # End the conversation
    except Exception as e:
        logger.error(f"Error in cancel_update for user {update.message.from_user.id}: {e}")  # Log the error
        await update.message.reply_text("خطایی رخ داد. لطفا دوباره تلاش کنید.")
        return ConversationHandler.END  # End the conversation in case of error


def my_profile_handlers(bot):
    # Create the conversation handler
    bot.add_handler(CallbackQueryHandler(handle_button_click))

    my_profile_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("my_profile", my_profile)],
        states={
            UpdateProfileStates.NAME.value: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_name)],
            UpdateProfileStates.BIRTH_DATE.value: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_birth_date)],
            UpdateProfileStates.BIO.value: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_bio)],
            UpdateProfileStates.HEIGHT.value: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_height)],
            UpdateProfileStates.IMAGE.value: [MessageHandler(filters.PHOTO, update_image)],
            UpdateProfileStates.LOCATION.value: [MessageHandler(filters.LOCATION, update_location)],
        },
        fallbacks=[CommandHandler("cancel_update", cancel_update)],
    )

    # Add the conversation handler to the application
    bot.add_handler(my_profile_conv_handler)
