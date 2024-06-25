from pyrogram import filters
from main import app

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    text = """
apa si dek"""
    await message.reply(text)
  
