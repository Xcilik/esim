import asyncio
import sys
from atexit import register
from datetime import datetime, timedelta
from os import execl
from importlib import import_module
from main.modules import loadModule

from pyrogram import idle
from pytz import timezone

from main import *

LOOP = asyncio.get_event_loop()


async def loadPlugins():
    modules = loadModule()
    for mod in modules:
        imported_module = import_module(f"main.modules.{mod}")

    console.info("Plugins installed")


async def main():
    await app.start()

    console.info("Bot Running")
    await asyncio.gather(loadPlugins(), idle())


if __name__ == "__main__":
    LOOP.run_until_complete(main())
    console.info("Bot Stoped")
