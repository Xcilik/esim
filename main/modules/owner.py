import os
import random
import subprocess
import sys
import traceback
from asyncio import sleep
from io import BytesIO, StringIO
from subprocess import PIPE, Popen, TimeoutExpired
from time import perf_counter

from aiofiles import open as aopen
from aiofiles.os import remove as aremove
from pyrogram import filters
from pyrogram.errors import FloodWait
from main import app
from config import OWNER_ID

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "\n c = cilik = client"
        + "\n m = message"
        + "\n r = message.reply_to_message"
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)
    

@app.on_message(filters.command("update") & filters.user(OWNER_ID))
async def update(_, message):
    try:
        out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
        if "Already up to date.." in str(out):
            return await message.reply_text("Its already up-to date!")
        await message.reply_text(f"{out}")
    except Exception as e:
        return await message.reply_text(str(e))
    await message.reply_text("<b>Updated with default branch, restarting now.</b>")
    os.execl(sys.executable, sys.executable, "-m", "main")


@app.on_message(filters.command("eval|ev") & filters.user(OWNER_ID))
async def evaluate(client, message):
    try:
        cmd = message.text.split(None, maxsplit=1)[1]
    except:
        return await message.reply("乁⁠(⁠ ⁠•⁠_⁠•⁠ ⁠)⁠ㄏ")
    old_stderr = sys.stderr

    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = f"<b>Output</b>:\n    <code>{evaluation.strip()}</code>"
    if len(final_output) > 4096:
        filename = "output.txt"
        async with aopen(filename, "w+", encoding="utf8") as out_file:
            await out_file.write(str(final_output))
        await message.reply_document(
            document=filename,
            caption=cmd,
            disable_notification=True,
            quote=True,
        )
        await aremove(filename)
    else:
        await message.reply(final_output)




