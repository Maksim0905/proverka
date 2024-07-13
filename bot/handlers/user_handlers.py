import asyncio
import logging
from aiogram import BaseMiddleware
from aiogram import types, Dispatcher, Bot
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, ContentType, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery,InputMedia, InputMediaPhoto, InputMediaVideo, InputMediaAudio, InputMediaDocument, InputMediaAnimation
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram.fsm.state import State, StatesGroup
from bot.utils.utils import generate_random_string
from datetime import datetime, timedelta
from aiogram.enums import ParseMode
import bot.functions.db_functions as fn
import bot.keyboards.user_keyboards as kb


user_router = Router()


class AddArt(StatesGroup):
    msg_id = State()
    name = State()
    about = State()
    era = State()
    country = State()
    photo = State()


class AddFilterEra(StatesGroup):
    waiting_era_filter = State()

class AddFilterCountry(StatesGroup):
    waiting_country_filter = State()


class AddFilterAbout(StatesGroup):
    waiting_about_filter = State()


@user_router.message(CommandStart())
async def send_welcome(message: types.Message):
    chat_id = message.chat.id
    text = 'Добро пожаловать, в систему для управления обменом культурными артефактами между музеями\n'
    text += 'Для управления воспользуйтесь кнопками снизу!'
    await fn.first_join(chat_id)
    await message.answer(
        text = text,
        reply_markup=kb.start_keys
    )


@user_router.message(F.text == '🏛 Профиль')
async def profile(message: Message):
    """ Профиль пользователя
    """
    chat_id = message.from_user.id
    exponats = await fn.get_exponats(chat_id)
    username = f'museum-{chat_id}'
    text = f'🏛 Профиль музея: <code>{username}</code>\n'
    text += f'🏺 Кличество экспонатов: {len(exponats)}'
    await message.answer(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=kb.transactions
    )


@user_router.message(F.text == '➕ Добавить экспонат')
async def add_expo(message: Message, state: FSMContext):
    """Добавление имени к экспонату
    """
    msg = await message.answer(
        text='Введите название экспоната:',
        parse_mode=ParseMode.HTML,
        reply_markup=kb.back_keys
    )
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(AddArt.name)


@user_router.message(F.text == '🔄 Обмены')
async def exchange(message: Message, state: FSMContext):
    """Меню обменов
    """
    chat_id = message.from_user.id
    data = await fn.get_filtered_artifacts(chat_id)
    print(data)
    keyboard = []
    try:
        for name in data:
            keyboard.append([InlineKeyboardButton(text=name[1], callback_data=f'ch*{name[0]}')])
    except:
        pass
    keyboard.append([InlineKeyboardButton(text='⚙️ Фильтры', callback_data='filters')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    msg = await message.answer(
        text='Выберите экспонат',
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )


@user_router.callback_query(F.data.startswith('ch'))
async def get_artefact(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Получение информации об экспонате
    """
    artefact_id = callback.data.split('*')[1]
    data = await fn.get_artefact(artefact_id)
    print(data)
    text = f'Владелец: <code>{data[1]}</code>\n\n'
    text += f'Название: {data[2]}\n'
    text += f'Описание: {data[3]}\n'
    text += f'Эра: {data[4]}\n'
    text += f'Страна: {data[5]}\n'
    await callback.message.delete()
    await bot.send_photo(chat_id=callback.from_user.id, photo=data[6], caption=text, parse_mode=ParseMode.HTML, reply_markup=kb.change_keyboard(data[0]))


@user_router.callback_query(F.data.startswith('change'))
async def change_artefact(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Обмен экспоната
    """
    artefact_id = callback.data.split('_')[1]
    await callback.message.edit_text(
        text='Вы не загрузили экспонат или он ваш!',
        parse_mode=ParseMode.HTML
    )


@user_router.callback_query(F.data == 'back_change')
async def back_change(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Возврат к списку экспонатов
    """
    chat_id = callback.from_user.id
    data = await fn.get_filtered_artifacts(chat_id)
    print(data)
    keyboard = []
    try:
        for name in data:
            keyboard.append([InlineKeyboardButton(text=name[1], callback_data=f'ch*{name[0]}')])
    except:
        pass
    keyboard.append([InlineKeyboardButton(text='⚙️ Фильтры', callback_data='filters')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await callback.message.delete()
    await callback.message.answer(
        text='Выберите экспонат',
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )


@user_router.callback_query(F.data == 'filters')
async def filters(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Фильтры
    """
    await callback.message.edit_text(
        text='Выберите фильтр',
        parse_mode=ParseMode.HTML,
        reply_markup=kb.filter_kb
    )


@user_router.callback_query(F.data.startswith('fl'))
async def get_filter(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Получение информации об экспонате
    """
    chat_id = callback.from_user.id
    filter = callback.data.split('_')[1]
    if filter == 'reset':
        await fn.delete_filters(chat_id)
        await callback.answer('Фильтры сброшены', show_alert=False)

    elif filter == 'era':
        await callback.message.edit_text(
            text='Введите эру\n\nДля отмены введите <code>❌ Отмена</code>',
            parse_mode=ParseMode.HTML
        )
        await state.set_state(AddFilterEra.waiting_era_filter)
    
    elif filter == 'country':
        await callback.message.edit_text(
            text='Введите страну\n\nДля отмены введите <code>❌ Отмена</code>',
            parse_mode=ParseMode.HTML
        )
        await state.set_state(AddFilterCountry.waiting_country_filter)
    
    elif filter == 'about':
        await callback.message.edit_text(
            text='Введите описание\n\nДля отмены введите <code>❌ Отмена</code>',
            parse_mode=ParseMode.HTML
        )
        await state.set_state(AddFilterAbout.waiting_about_filter)


@user_router.message(AddFilterAbout.waiting_about_filter)
async def filter_about(message: Message, state: FSMContext, bot: Bot):
    """Фильтр по описанию
    """
    chat_id = message.from_user.id
    if message.text == '❌ Отмена':
        await state.clear()
        await message.answer('Отменено', reply_markup=kb.start_keys)
        await message.delete()
    else:
        about = message.text
        await fn.filter_about(chat_id, about)
        await message.answer('Фильтр по описанию установлен', reply_markup=kb.filter_kb)
        await state.clear()


@user_router.message(AddFilterCountry.waiting_country_filter)
async def filter_country(message: Message, state: FSMContext, bot: Bot):
    """Фильтр по стране
    """
    chat_id = message.from_user.id
    if message.text == '❌ Отмена':
        await state.clear()
        await message.answer('Отменено', reply_markup=kb.start_keys)
        await message.delete()
    else:
        country = message.text
        await fn.filter_country(chat_id, country)
        await message.answer('Фильтр по стране установлен', reply_markup=kb.filter_kb)
        await state.clear()


@user_router.message(AddFilterEra.waiting_era_filter)
async def filter_era(message: Message, state: FSMContext, bot: Bot):
    """Фильтр по эре
    """
    chat_id = message.from_user.id
    if message.text == '❌ Отмена':
        await state.clear()
        await message.answer('Отменено', reply_markup=kb.start_keys)
        await message.delete()
    else:
        era = message.text
        await fn.filter_era(chat_id, era)
        await message.answer('Фильтр по эре установлен', reply_markup=kb.filter_kb)
        await state.clear()





@user_router.message(AddArt.name)
async def add_expo_about(message: Message, state: FSMContext, bot: Bot):
    """Добавление описания к экспонату
    """
    chat_id = message.from_user.id
    if message.text == '❌ Отмена':
        await state.clear()
        await message.answer('Отменено', reply_markup=kb.start_keys)
        await message.delete()
    else:
        msg_id = (await state.get_data())['msg_id']
        await bot.delete_message(chat_id=chat_id, message_id=msg_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        msg = await message.answer('Введите описание:', reply_markup=kb.back_keys)
        await state.update_data(msg_id=msg.message_id)
        await state.update_data(name=message.text)
        await state.set_state(AddArt.about)


@user_router.message(AddArt.about)
async def add_expo_era(message: Message, state: FSMContext, bot: Bot):
    """Добавление эры к экспонату
    """
    chat_id = message.from_user.id
    if message.text == '❌ Отмена':
        await state.clear()
        await message.answer('Отменено', reply_markup=kb.start_keys)
        await message.delete()
    else:
        msg_id = (await state.get_data())['msg_id']
        await bot.delete_message(chat_id=chat_id, message_id=msg_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        msg = await message.answer('Введите эру:', reply_markup=kb.back_keys)
        await state.update_data(msg_id=msg.message_id)
        await state.update_data(about=message.text)
        await state.set_state(AddArt.era)


@user_router.message(AddArt.era)
async def add_expo_country(message: Message, state: FSMContext, bot: Bot):
    """Добавление страны к экспонату
    """
    chat_id = message.from_user.id
    if message.text == '❌ Отмена':
        await state.clear()
        await message.answer('Отменено', reply_markup=kb.start_keys)
        await message.delete()
    else:
        msg_id = (await state.get_data())['msg_id']
        await bot.delete_message(chat_id=chat_id, message_id=msg_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        msg = await message.answer('Введите страну:', reply_markup=kb.back_keys)
        await state.update_data(msg_id=msg.message_id)
        await state.update_data(era=message.text)
        await state.set_state(AddArt.country)


@user_router.message(AddArt.country)
async def add_expo_photo(message: Message, state: FSMContext, bot: Bot):
    """Добавление фото к экспонату
    """
    chat_id = message.from_user.id
    if message.text == '❌ Отмена':
        await state.clear()
        await message.answer('Отменено', reply_markup=kb.start_keys)
        await message.delete()
    else:
        msg_id = (await state.get_data())['msg_id']
        await bot.delete_message(chat_id=chat_id, message_id=msg_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        msg = await message.answer('Пришлите фото:', reply_markup=kb.back_keys)
        await state.update_data(msg_id=msg.message_id)
        await state.update_data(country=message.text)
        await state.set_state(AddArt.photo)


@user_router.message(AddArt.photo)
async def add_expo_result(message: Message, state: FSMContext, bot: Bot):
    """Вывод итогового результата
    """
    chat_id = message.from_user.id
    if message.text == '❌ Отмена':
        await state.clear()
        await message.answer('Отменено', reply_markup=kb.start_keys)
        await message.delete()
    else:
        msg_id = (await state.get_data())['msg_id']
        await bot.delete_message(chat_id=chat_id, message_id=msg_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        photo_id = message.photo[-1].file_id
        id = generate_random_string()
        await fn.add_artefact_trash(id,
                                     f'{(await state.get_data())["name"]}*{(await state.get_data())["about"]}*{(await state.get_data())["era"]}*{(await state.get_data())["country"]}*{photo_id}')
        await message.answer_photo(
            photo=photo_id,
            caption=f'Название: {(await state.get_data())["name"]}\n'
                    f'Описание: {(await state.get_data())["about"]}\n'
                    f'Эра: {(await state.get_data())["era"]}\n'
                    f'Cтрана: {(await state.get_data())["country"]}\n',
            reply_markup=kb.generate_keyboard(id)
        )
        await state.clear()


@user_router.callback_query(F.data.startswith('add_art'))
async def add_art(callback: CallbackQuery, bot: Bot):
    """ Добавление экспоната в базу
    """
    chat_id = callback.from_user.id
    id = callback.data.split('-')[1]
    data = await fn.get_artefact_trash(id)
    name, about, era, country, photo = tuple((await fn.get_artefact_trash(id))[0].split('*'))
    # print(name, about, era, country, photo)
    await fn.add_expo(chat_id, name, about, era, country, photo)
    await callback.message.answer('✅ Экспонат успешно добавлен', reply_markup=kb.start_keys)
    await bot.delete_message(chat_id=chat_id, message_id=callback.message.message_id)


@user_router.callback_query(F.data == 'delete_previev')
async def del_art(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    await callback.message.answer('❌ Черновик удалён', reply_markup=kb.start_keys)


@user_router.callback_query(F.data == 'transaction')
async def transaction(callback: CallbackQuery):
    chat_id = callback.from_user.id
    await callback.message.answer(
        text='Транзакции отсутствуют',
        parse_mode=ParseMode.HTML
    )


@user_router.callback_query(F.data == 'my_expo')
async def back(callback: CallbackQuery):
    chat_id = callback.from_user.id
    # TODO: Добавить вывод экспонатов

