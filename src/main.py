import logging

from pyrogram import Client, filters

from config import API_HASH, API_ID, BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Client("DelalehBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.command("start"))
async def start(client, message):
    user = message.from_user
    logger.info(f"New user started the bot: {user.first_name} ({user.id})")
    await message.reply(f"Hello, {user.first_name}! Welcome to the bot. 😊")


app.run()
