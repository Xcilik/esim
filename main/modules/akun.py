from pyrogram import filters
from main import app
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@app.on_message(filters.command("setting") & filters.private)
async def setting(client, message):
    text = f"""
"""    
    button = [
        [
            InlineKeyboardButton("Tambah Akun", callback_data="add_akun"),
        ],
        [
           InlineKeyboardButton("Setting", callback_data="setting"),
        ],
    ]
