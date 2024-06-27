from pyrogram import filters
from main import app, akun
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Button:
    def user_akun(user_id, count):
        button = [
            [
                InlineKeyboardButton(
                    "Hapus",
                    callback_data=f"hapus_akun {int(count)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "Cek Nomor",
                    callback_data=f"get_phone {int(count)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "Cek Otp",
                    callback_data=f"get_otp {int(count)}",
                )
            ],
            [
                InlineKeyboardButton("❮", callback_data=f"prev_akun {int(count)}"),
                InlineKeyboardButton("❯", callback_data=f"next_akun {int(count)}"),
            ],
            [
                InlineKeyboardButton("Tutup", callback_data=f"0_cls"),
            ],
        ]
        return button

        
@app.on_message(filters.regex("^(prev_ub|next_ub)"))
async def next_prev_akun(client, callback_query):
    query = callback_query.data.split()
    count = int(query[1])
    if query[0] == "next_akun":
        if count == len(akun._akun) - 1:
            count = 0
        else:
            count += 1
    elif query[0] == "prev_akun":
        if count == 0:
            count = len(akun._akun) - 1
        else:
            count -= 1
            
    await callback_query.edit_message_text(f"""
<b>Akun Ke</b> <code>{int(count) + 1}/{len(akun._akun)}</code>
<b>Name:</b> <a href=tg://user?id={ubot._ubot[int(count)].me.id}>{akun._akun[int(count)].me.first_name} {akun._akun[int(count)].me.last_name or ''}</a> 
<b>Id:</b> <code>{akun._akun[int(count)].me.id}</code>
""",
        reply_markup=InlineKeyboardMarkup(
            Button.user_akun(akun._akun[count].me.id, count)
        ),
    )
    

@app.on_callback_query(filters.regex("^(get_otp|get_phone|hapus_akun)"))
async def tools(client, callback_query):
    query = callback_query.data.split()
    X = akun._akun[int(query[1])]
    if query[0] == "get_otp":
        async for otp in X.search_messages(777000, limit=1):
            try:
                if not otp.text:
                    await callback_query.answer("❌ Kode tidak ditemukan", True)
                else:
                    await callback_query.edit_message_text(
                        otp.text,
                        reply_markup=InlineKeyboardMarkup(
                            Button.user_akun(X.me.id, int(query[1]))
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
                    Button.user_akun(X.me.id, int(query[1]))
                ),
            )
        except Exception as error:
            return await callback_query.answer(error, True)
    elif query[0] == "hapus_akun":
        get_mention = f"<b><a href=tg://user?id={X.me.id}>{X.me.id}</a></b>"
        try:
            await X.log_out()
            return await callback_query.edit_message_text(
                f"✅ nokos <code>{X.me.id}</code> sudah dimatikan",
                reply_markup=InlineKeyboardMarkup(
                    Button.user_akun(X.me.id, int(query[1]))
                ),
            )
        except Exception as error:
            return await callback_query.answer(error, True)

@app.on_message(filters.command("cek") & filters.private)
async def cek(client, message):
    try:
        text = f"""
<b>Akun Ke</b> <code>{0 + 1}/{len(akun._akun)}</code>
<b>Name:</b> <a href=tg://user?id={akun._akun[0].me.id}>{akun._akun[0].me.first_name} {akun._akun[0].me.last_name or ''}</a> 
<b>Id:</b> <code>{akun._akun[0].me.id}</code>
"""    
        await app.send_message(message.chat.id, text,
            reply_markup=InlineKeyboardMarkup(Button.user_akun(akun._akun[0].me.id, 0)),
        )
    except:
        await app.send_message(message.chat.id, "Gada akun dek")
