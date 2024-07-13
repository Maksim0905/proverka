from aiogram import types, Bot
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram import F, Router
import bot.keyboards.admin_keyboards as kb
from bot.config import admins


admin_router = Router()


@admin_router.message(Command('admin'))
async def admin(message: types.Message, bot: Bot):
    chat_id = message.from_user.id
    if chat_id in admins:
        await message.answer("Добро пожаловать в админ панель!", reply_markup=kb.reuests)


@admin_router.callback_query(F.data == 'requests')
async def req(callback: CallbackQuery):
    await callback.answer('💤 Заявки отсутствуют', show_alert=False)
