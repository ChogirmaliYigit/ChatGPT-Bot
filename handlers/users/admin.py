import asyncio
from aiogram import types
from data.config import ADMINS
from loader import dp, db, bot
from states.main import ChatState
from aiogram.dispatcher import FSMContext
from keyboards.default.main import get_chat_list
import pandas as pd

@dp.message_handler(text="/allusers", user_id=ADMINS, state="*")
async def get_all_users(message: types.Message):
    users = await db.select_all_users()
    id = []
    name = []
    for user in users:
        id.append(user["telegram_id"])
        name.append(user["full_name"])
    data = {
        "Telegram ID": id,
        "Name": name
    }
    pd.options.display.max_rows = 10000
    df = pd.DataFrame(data)
    if len(df) > 50:
        for x in range(0, len(df), 50):
            await bot.send_message(message.chat.id, df[x:x + 50])
    else:
       await bot.send_message(message.chat.id, df)
       

@dp.message_handler(text="/reklama", user_id=ADMINS, state="*")
async def send_ad_to_all(message: types.Message):
    try:
        users = await db.select_all_users()
        for user in users:
            await bot.send_message(chat_id=user["telegram_id"], text="<b>@BekoDev kanaliga obuna bo'lib yangiliklardan xabardor bo'ling!</b>", parse_mode="html")
            await asyncio.sleep(0.05)
    except Exception as error:
        await message.answer(f"Uzur xatolik yuz berdi keyinroq urinib ko'ring\n<b>{error}</b>", parse_mode="html")
    finally:
        await message.answer("Xabar jo'natildi")

@dp.message_handler(text="/update", user_id=ADMINS, state="*")
async def send_update_to_all(message: types.Message):
    try:
        users = await db.select_all_users()
        for user in users:
            await bot.send_message(chat_id=user["telegram_id"], text="<b>Botga yangi imkoniyatlar qo'shildi! Uni sinab ko'rishingiz mumkin!</b>", parse_mode="html")
            await asyncio.sleep(0.05)
    except Exception as error:
        await message.answer(f"Uzur xatolik yuz berdi keyinroq urinib ko'ring\n<b>{error}</b>", parse_mode="html")
    finally:
        await message.answer("Xabar jo'natildi")

@dp.message_handler(text="🖼 Post Ulashish", user_id=ADMINS, state="*")
async def repost_message(message: types.Message):
    await message.answer("Foydalanuvchilarga jo'natmoqchi bo'lgan xabarni botga yuboring")
    await ChatState.repost.set()

@dp.message_handler(content_types=types.ContentTypes.ANY, user_id=ADMINS, state=ChatState.repost)
async def send_post_all_groups(message: types.Message, state: FSMContext):
    try:
        users = await db.select_all_users()
        for user in users:
            await message.send_copy(chat_id=user["telegram_id"])
            await asyncio.sleep(0.05)
    except Exception as error:
        await message.answer(f"Uzur xatolik yuz berdi keyinroq urinib ko'ring\n<b>{error}</b>", parse_mode="html")
    finally:
        user = await db.select_user(telegram_id=message.from_user.id)
        await message.answer("Post jo'natildi", reply_markup=await get_chat_list(user_id=user["id"]))
        await state.finish()

@dp.message_handler(text="/cleandb", user_id=ADMINS)
async def get_all_users(message: types.Message):
    await db.delete_users()
    await message.answer("Baza tozalandi!")
