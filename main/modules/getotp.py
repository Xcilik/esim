import requests
import asyncio
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from main import app


api_id = 394  
api_key = "GACHAbQOhNNsWGz4PXVlVMiGNunQm7I9wB79b8Gkn3At2XsFfHGa2PKyUZQ7dGXG"  


@app.on_message(filters.command("get") & filters.private)
async def get(client, message):
    text = f"""
Silahkan pilih Kategori
"""
    button = [
        [
            InlineKeyboardButton("Telegram", callback_data="buy_nokos telegram"),
            InlineKeyboardButton("WhatsApp", callback_data="buy_nokos whatsapp"),
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

    params = {
        "api_id": api_id,
        "api_key": api_key,
        "country": int(data[2]),
        "service": int(data[1]),
        "operator": "any"
    }

    try:
        response = requests.post(url, json=params)
        json_data = response.json()
        
        if not json_data['success']:
            raise Exception(json_data['data'])
        
        order_id = json_data['data']['order_id']
        country_name = json_data['data']['country_name']
        service_name = json_data['data']['service_name']
        phone = json_data['data']['phone']
        expired_at = json_data['data']['expired_at']
        
        text = f"""
OTP {service_name}
#{order_id}

Nomor: `{phone}`
Negara: {country_name}
Waktu Expired: {expired_at}
"""
        button = [
            [
                InlineKeyboardButton("💌 Cek OTP", callback_data=f"refresh {order_id}"),
            ],
            [
                InlineKeyboardButton("🔁 Ganti", callback_data=f"ganti {order_id} {int(data[1])} {int(data[2])}"),
                InlineKeyboardButton("✅ Succes", callback_data=f"succes {order_id}"),
                InlineKeyboardButton("📩 Resend", callback_data=f"resend {order_id}"),    
            ],
            [
                InlineKeyboardButton("❌ Cancel", callback_data=f"cancel {order_id}"),
            ],
        ]        
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(button))
    except Exception as e:
        error_message = str(e)
        if error_message in [
            "API salah atau tidak aktif", 
            "NO SERVICE", 
            "QUEUE LIMIT", 
            "NO BALANCE", 
            "SERVER MAINTENANCE", 
            "NO NUMBERS", 
            "SERVER OFF"
        ]:
            try:
                five_sim_response = await handle_five_sim_order(data[1], data[2])
                # Format text for 5sim response
                text = f"""
OTP {five_sim_response['product']}
#{five_sim_response['id']}

Nomor: `{five_sim_response['phone']}`
Negara: {five_sim_response['country']}
Waktu Expired: {five_sim_response['expires']}
"""
                await callback_query.edit_message_text(text)
            except Exception as five_sim_error:
                await callback_query.edit_message_text(f"Error: {str(five_sim_error)}")
        else:
            await callback_query.edit_message_text(f"Error: {error_message}")



@app.on_callback_query(filters.regex("refresh|cancel|resend|succes|ganti"))
async def atur(client, callback_query):
    data = callback_query.data.split()
    if data[0] == "refresh":
        
        url = "https://litensi.id/api/sms/getstatus"
        params = {
            "api_id": api_id,
            "api_key": api_key,
            "order_id": int(data[1]),

        }
        await asyncio.sleep(5)
        response = requests.post(url, json=params)
        json_data = response.json()
        text = f"Kode OTP: {json_data['data']['sms']}"
        button = [
            [
               InlineKeyboardButton("💌 Cek OTP", callback_data=f"refresh {int(data[1])}"),
            ],
        ]
            
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(button))
    elif data[0] == "cancel":
        url = "https://litensi.id/api/sms/setstatus"
        params = {
            "api_id": api_id,
            "api_key": api_key,
            "order_id": int(data[1]),
            "status": "CANCELED"
        }
        response = requests.post(url, json=params)
        json_data = response.json()
        text = f"CANCEL\n\n{json_data}"
        await callback_query.edit_message_text(text)        
