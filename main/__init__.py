import logging
import os
import re
import subprocess
import sys
from typing import Callable
from telethon.sync import TelegramClient


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
logging.getLogger("telethon").setLevel(logging.ERROR)
logging.getLogger("pyrogram.session.session").setLevel(logging.WARNING)


console = logging.getLogger(__name__)

"""class Akun(Client):
    __module__ = "pyrogram.client"
    _akun = []
    _get_my_id = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs, device_model="Telegram")

  
    async def start(self):
        await super().start()
        self._akun.append(self)
        self._get_my_id.append(self.me.id)
        console.info(f"Starting Akun {self.me.id}|{self.me.first_name}")
"""


app = Client(
    name="akun",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

