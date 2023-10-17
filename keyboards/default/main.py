from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from loader import db
from data.config import BACKEND_URL, ADMINS

async def get_chat_list(user_id):
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(KeyboardButton(text="➕ Yangi Chat"))
    markup.add(KeyboardButton(text="📝 Chatlar tarixi", web_app=WebAppInfo(url=f"{BACKEND_URL}/chat/{user_id}/")))
    user = await db.select_user(id=user_id)
    if str(user["telegram_id"]) in ADMINS:
        markup.add(KeyboardButton(text="🙋‍♂️ Admin Panel", web_app=WebAppInfo(url=f"{BACKEND_URL}/admin/")))
        markup.add(KeyboardButton(text="🖼 Post Ulashish"))
    return markup

finish = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
finish.row("❌ Chatni yakunlash")
