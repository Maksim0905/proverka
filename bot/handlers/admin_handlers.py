import asyncio
import logging
from aiogram import BaseMiddleware
from aiogram import types, Dispatcher, Bot
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, ContentType, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto, InputMediaVideo, InputMediaAudio, InputMediaDocument, InputMediaAnimation
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram.fsm.state import State, StatesGroup
import math
import os
from datetime import datetime, timedelta
from aiogram.enums import ParseMode
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