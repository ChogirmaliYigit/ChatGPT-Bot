import asyncio
from aiogram import types
from utils.chat_gpt import get_response
from loader import dp, bot, db
from aiogram.dispatcher import FSMContext
from states.main import ChatState
from keyboards.default.main import get_chat_list


@dp.message_handler(state=ChatState.content, text="❌ Chatni yakunlash")
async def finish_chat(message: types.Message, state: FSMContext):
    await state.finish()
    user = await db.select_user(telegram_id=message.from_user.id)
    await message.answer("<b>Men sizni qiziqtirgan mavzu bo'yicha yordam berishim mumkin!</b>", parse_mode="html", reply_markup=await get_chat_list(user["id"]))


# Chat GPT Bot
@dp.message_handler(state=ChatState.content)
async def chat_gpt_response(message: types.Message, state: FSMContext):
    data = await state.get_data()
    chat_id = data.get("chat_id")
    await db.add_message(content=message.text, role="user", chat_id=chat_id)

    chat_messages = await db.select_messages(chat_id=chat_id)
    messages = []
    for chat_message in chat_messages:
        messages.append({"role": chat_message["role"], "content": chat_message['content']})

    chat = await message.answer(text='⌛️')
    message_id = chat.message_id

    response = get_response(messages=messages)
    await bot.edit_message_text(text=response, chat_id=message.chat.id, message_id=message_id)
    
    chat_db = await db.select_chat(id=chat_id)
    if chat_db["title"] is None:
        await db.update_chat_title(chat_id=chat_id, title=message.text)
    await db.add_message(content=response, role="assistant", chat_id=chat_id)
