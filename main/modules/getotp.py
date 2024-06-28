import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from main import app

@app.on_message(filters.command("get") & filters.private)
async def get(client, message):
    text = f"""
Silahkan pilih Kategori
"""
    button = [
        [
            InlineKeyboardButton("Telegram", callback_data=""),
            InlineKeyboardButton("WhatsApp", callback_data=""),
        ],
        [
            InlineKeyboardButton("Instagram", callback_data=""),
            InlineKeyboardButton("Facebook", callback_data=""),
        ],
        [
            InlineKeyboardButton("Twitter/X", callback_data=""),
            InlineKeyboardButton("Tokopedia", callback_data=""),
        ],
        [
            InlineKeyboardButton("Shopee", callback_data=""),
            InlineKeyboardButton("Lazada", callback_data=""),
        ],  
    ]
    await message.reply(text, reply_markup=InlineKeyboardMarkup(button))


@app.on_callback_query(filters.regex("buy_nokos"))
async def buy_nokos(client, callback_query):
    data = callback_query.data.split()
    
  
     
