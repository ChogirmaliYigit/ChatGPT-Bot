from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, db, bot
from data.config import ADMINS
from states.main import ChatState
from keyboards.default.main import get_chat_list, finish
from aiogram.dispatcher import FSMContext


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    name = message.from_user.username
    full_name = message.from_user.full_name
    if name is None:
        name = full_name
    else:
        name = f"@{name}"
    user = await db.select_user(telegram_id=message.from_user.id)
    if user is None:
        user = await db.add_user(
            telegram_id=message.from_user.id,
            full_name=full_name,
            username=message.from_user.username,
        )
        # ADMINGA xabar beramiz
        count = await db.count_users()
        msg = f"{name} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
        await bot.send_message(chat_id=ADMINS[0], text=msg)
    # user = await db.select_user(telegram_id=message.from_user.id)
    else:
        await bot.send_message(chat_id=ADMINS[0], text=f"{name} bazaga oldin qo'shilgan")
    await message.answer(f"Assalomu aleykum <b>{full_name}</b>!\n\n<i>Xush kelibsiz sizni qiziqtirgan mavzu bo'yicha yordam berishim mumkin!</i>", parse_mode=types.ParseMode.HTML, reply_markup=await get_chat_list(user["id"]))


@dp.message_handler(text="➕ Yangi Chat", state="*")
async def create_chat(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>Qiziqtirgan savolingiz bo'lsa menga yozishingiz mumkin!</b>", parse_mode="html", reply_markup=finish)
    user = await db.select_user(telegram_id=message.from_user.id)
    chat = await db.add_chat(user_id=user["id"])
    await state.update_data({"chat_id": chat['id']})
    await ChatState.content.set()


@dp.message_handler(text="📝 Chatlar tarixi", state="*")
async def history_chat(message: types.Message, state: FSMContext):
    await message.answer("<i>Uzur, hozircha chatlar tarixini ko'ra olmaysiz. Bu qism tez orada ishga tushiriladi!</i>", parse_mode='html')