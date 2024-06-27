import asyncio
from asyncio import get_event_loop_policy

import sys
from atexit import register
from datetime import datetime, timedelta
from os import execl
from importlib import import_module
from main.database import get_all_akun, remove_akun
from main.modules import loadModule

from pyrogram.errors import RPCError
from pyrogram import idle
from pytz import timezone

from main import *

LOOP = asyncio.get_event_loop()


async def loadPlugins():
    modules = loadModule()
    for mod in modules:
        imported_module = import_module(f"main.modules.{mod}")

    console.info("Plugins installed")




async def start_akun(user_id, _akun):
    akun_ = Akun(**_akun)
    try:
        await asyncio.wait_for(akun_.start(), timeout=30)
    except RPCError:
        await remove_akun(user_id)
        console.info(f"✅ {user_id} dihapus dari Database")
    except:
        pass


async def main():
    await app.start()
    console.info("Bot Running")

    await asyncio.gather(loadPlugins(), idle())


if __name__ == "__main__":
    get_event_loop_policy().get_event_loop().run_until_complete(main())
    console.info("Bot Stoped")
