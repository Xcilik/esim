import logging
import os
import re
import subprocess
import sys
from typing import Callable

import pyrogram
from aiofiles.os import remove as aremove
from aiofiles.ospath import exists as aexists
from aiohttp import ClientSession
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.handlers import MessageHandler
from pyromod import listen


from config import (API_ID, API_HASH, BOT_TOKEN)

aiohttpsession = ClientSession()

logging.basicConfig(
    level=logging.INFO,
    format="[ %(levelname)s ] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
    ],
)

logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pyrogram.session.session").setLevel(logging.WARNING)


console = logging.getLogger(__name__)

class Bot(Client):
    def __init__(self):
        console.info(f"Starting Bot")
        super().__init__(
            "nokos",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        await self.send_message(
                "greyvbss", "Bot nokos Started"
            )
        if get_me.last_name:
            self.name = get_me.first_name + " " + get_me.last_name
        else:
            self.name = get_me.first_name
        console.info(f"Bot Started as {self.name}")




app = Bot()
