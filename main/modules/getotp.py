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
            InlineKeyboardButton("Telegram", callback_data="buy_nokos telegram"),
            InlineKeyboardButton("WhatsApp", callback_data="buy_nokosbwhatsapp"),
        ],
        [
            InlineKeyboardButton("Instagram", callback_data="buy_nokos instagram"),
            InlineKeyboardButton("Facebook", callback_data="buy_nokos facebook"),
        ],
        [
            InlineKeyboardButton("Twitter/X", callback_data="buy_nokos twitter"),
            InlineKeyboardButton("Tokopedia", callback_data="buy_nokos tokopedia"),
        ],
        [
            InlineKeyboardButton("Shopee", callback_data="buy_nokos shopee"),
            InlineKeyboardButton("Lazada", callback_data="buy_nokos lazada"),
        ],  
        [
            InlineKeyboardButton("Tiktok", callback_data="buy_nokos tiktok"),
        ],          
    ]
    await message.reply(text, reply_markup=InlineKeyboardMarkup(button))


@app.on_callback_query(filters.regex("buy_nokos"))
async def buy_nokos(client, callback_query):
    data = callback_query.data.split()
    
    if data[1] == "telegram":
        id_sosmed = 187
    elif data[1] == "whatsapp":
        id_sosmed = 51
    elif data[1] == "instagram":
        id_sosmed = 61
    elif data[1] == "facebook":
        id_sosmed = 532   
    elif data[1] == "twitter":
        id_sosmed = 58  
    elif data[1] == "tokopedia":
        id_sosmed = 548       
    elif data[1] == "shopee":
        id_sosmed = 455
    elif data[1] == "lazada":
        id_sosmed = 363
    elif data[1] == "tiktok":
        id_sosmed = 478    
        
    text = "Silahkan pilih Negara"        
    button = [
        [
            InlineKeyboardButton("Indonesia", callback_data=f"post_requests {id_sosmed} 7"),
            InlineKeyboardButton("Canada", callback_data=f"post_requests {id_sosmed} 37"),
        ],
        [
            InlineKeyboardButton("Malaysia", callback_data=f"post_requests {id_sosmed} 8"),
            InlineKeyboardButton("Usa", callback_data=f"post_requests {id_sosmed} 13"),
        ],
    ]
    await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(button))
        
    


@app.on_callback_query(filters.regex("post_requests"))
async def post_requests(client, callback_query):
    data = callback_query.data.split()
    text = "Silahkan Tunggu"
    url = "https://litensi.id/api/sms/order"
    
    api_id = 394  
    api_key = "GACHAbQOhNNsWGz4PXVlVMiGNunQm7I9wB79b8Gkn3At2XsFfHGa2PKyUZQ7dGXG"  

    params = {
        "api_id": api_id,
        "api_key": api_key,
        "country": int(data[2]),
        "service": int(data[1]),
        "operator": "any"
    }
    try:
        response = requests.post(url, json=params)
        data = response.json()
        await callback_query.edit_message_text(text + f"\n\n{data}")
    except Exception as e:
        await callback_query.edit_message_text(f"rusak {str(e)}")
