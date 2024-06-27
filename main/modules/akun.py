from asyncio import TimeoutError

from pyrogram.errors import *

from pyrogram import filters
from main import app, akun
from config import API_ID, API_HASH
from main.database import add_akun
from main import *
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)



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



@app.on_message(filters.command("add") & filters.private)
async def add_akun(client, message):
    user_id = message.from_user.id
    try:
        contact_button = KeyboardButton("Kirim Nomor", request_contact=True)
        reply_markup = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True)
        phone = await client.ask(
            user_id,
            ("Silakan kirim nomor telepon Anda dengan mengklik tombol di bawah ini."),
            reply_markup=reply_markup,
            timeout=300,
        )
    except TimeoutError:
        return await client.send_message(user_id, "Waktu telah habis")
    phone_number = phone.contact.phone_number
    new_client = Akun(
        name=str(message.id),
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=False,
    )
    get_otp = await client.send_message(
        user_id, "<i>Mengirim kode OTP...</i>", reply_markup=ReplyKeyboardRemove()
    )
    await new_client.connect()
    try:
        code = await new_client.send_code(phone_number)
    except FloodWait as FW:
        await get_otp.delete()
        return await client.send_message(user_id, FW)
    except ApiIdInvalid as AII:
        await get_otp.delete()
        return await client.send_message(user_id, AII)
    except PhoneNumberInvalid as PNI:
        await get_otp.delete()
        return await client.send_message(user_id, PNI)
    except PhoneNumberFlood as PNF:
        await get_otp.delete()
        return await client.send_message(user_id, PNF)
    except PhoneNumberBanned as PNB:
        await get_otp.delete()
        return await client.send_message(user_id, PNB)
    except PhoneNumberUnoccupied as PNU:
        await get_otp.delete()
        return await client.send_message(user_id, PNU)
    except Exception as error:
        await get_otp.delete()
        return await client.send_message(user_id, f"<b>ERROR:</b> {error}")
    try:
        await get_otp.delete()
        otp = await client.ask(
            user_id,
            (
                "OTP telah dikirim melalui aplikasi <a href=tg://openmessage?user_id=777000>Telegram</a>, Silakan masukkan OTP dalam format <code>1 2 3 4 5</code>.  <i>(Spasi di antara setiap angka!)</i>"
            ),
            timeout=300,
        )
    except TimeoutError:
        return await client.send_message(user_id, "Waktu telah habis")
    otp_code = otp.text
    try:
        await new_client.sign_in(
            phone_number.strip(),
            code.phone_code_hash,
            phone_code=" ".join(str(otp_code)),
        )
    except PhoneCodeInvalid as PCI:
        return await client.send_message(user_id, PCI)
    except PhoneCodeExpired as PCE:
        return await client.send_message(user_id, PCE)
    except BadRequest as error:
        return await client.send_message(user_id, f"<b>ERROR:</b> {error}")
    except SessionPasswordNeeded:
        try:
            two_step_code = await client.ask(
                user_id,
                "Akun Anda mengaktifkan verifikasi dua langkah.\nSilahkan masukkan kata sandi Anda.",
                timeout=300,
            )
        except TimeoutError:
            return await client.send_message(user_id, "Batas waktu tercapai 5 menit.")
        new_code = two_step_code.text
        try:
            await new_client.check_password(new_code)
        except Exception as error:
            return await client.send_message(user_id, f"<b>Error:</b> {error}")
    session_string = await new_client.export_session_string()
    await new_client.disconnect()
    new_client.storage.session_string = session_string
    new_client.in_memory = False
    await new_client.start()
    await add_akun(
        user_id=int(new_client.me.id),
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
    )
    for mod in loadModule():
        importlib.reload(importlib.import_module(f"main.modules.{mod}"))

    await client.send_message(
        user_id,
        "Done!",
    )



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
