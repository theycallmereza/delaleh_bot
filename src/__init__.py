import sys
import time
from asyncio import get_event_loop, new_event_loop, set_event_loop

from telegram.ext import Application

from src import config
from src.logging import LOGGER

LOGGER(__name__).info("Starting DelalehBot....")
BotStartTime = time.time()

if sys.version_info[0] < 3 or sys.version_info[1] < 7:
    LOGGER(__name__).critical(
        """
=============================================================
You MUST need to be on python 3.7 or above, shutting down the bot...
=============================================================
"""
    )
    sys.exit(1)

LOGGER(__name__).info("setting up event loop....")
try:
    loop = get_event_loop()
except RuntimeError:
    set_event_loop(new_event_loop())
    loop = get_event_loop()

LOGGER(__name__).info(
    r"""
  ___      _      _     _    ___      _
 |   \ ___| |__ _| |___| |_ | _ ) ___| |_
 | |) / -_) / _` | / -_) ' \| _ \/ _ \  _|
 |___/\___|_\__,_|_\___|_||_|___/\___/\__|
"""
)
# https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20


LOGGER(__name__).info("initiating the client....")
bot = Application.builder().token(config.BOT_TOKEN).build()
