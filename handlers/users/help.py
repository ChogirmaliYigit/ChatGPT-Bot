from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("<b>Buyruqlar ro'yhati: </b>",
            "\n/start - Botni ishga tushirish",
            "/help - Yordam",
            "\n🧑‍💻 <b>Dasturchi: @BekzodRakhimov</b>")
    
    await message.answer("\n".join(text), parse_mode="html")
