from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                            ReplyKeyboardMarkup, KeyboardButton)
from aiogram.types import BotCommand


async def setup_bot_commands(bot):
    bot_commands = [
        BotCommand(command="/start", description="Начало работы")
    ]
    await bot.set_my_commands(bot_commands)


start_keys = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='🏛 Профиль')],
              [KeyboardButton(text='➕ Добавить экспонат')],
              [KeyboardButton(text='🔄 Обмены')]],
              resize_keyboard=True,
              input_field_placeholder='Выбери пункт меню...')


transactions = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='📨 Транзакции', callback_data='transaction')],
        [InlineKeyboardButton(text='🏺 Мои Товары', callback_data='my_expo')]
    ]
)


back_keys = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='❌ Отмена')]],
              resize_keyboard=True,
              one_time_keyboard=True,
              input_field_placeholder='Для отмены нажмите ❌ Отмена')


def generate_keyboard(id):
    gk_keys = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='✅ ОК', callback_data=f'add_art-{id}'),
          InlineKeyboardButton(text='❌ Удалить', callback_data='delete_previev')]
    ])
    return gk_keys


def change_keyboard(id):
    ck_keys = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='⬅️ Назад', callback_data='back_change'),
          InlineKeyboardButton(text='🔄 Обменять', callback_data=f'change_{id}')]
    ])
    return ck_keys


filter_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Эра', callback_data='fl_era'), InlineKeyboardButton(text='Описание', callback_data='fl_about'), InlineKeyboardButton(text='Страна', callback_data='fl_country')],
        [InlineKeyboardButton(text='🆕 Сбросить фильтры', callback_data='fl_reset')],
        [InlineKeyboardButton(text='⬅️ Назад', callback_data='back_change')]
    ]
)


# def beautiful_filter(era=False, about=False, country=False):
#     if era:
#         filter_kb = InlineKeyboardMarkup(
#             inline_keyboard=[
#                 [InlineKeyboardButton(text='✅ Эпоха', callback_data='fl_epoch'), InlineKeyboardButton(text='Описание', callback_data='fl_about'), InlineKeyboardButton(text='Страна', callback_data='fl_country')],
#                 [InlineKeyboardButton(text='🆕 Сбросить фильтры', callback_data='fl_reset')]
#             ]
#         )
#     elif country:
#         filter_kb = InlineKeyboardMarkup(
#             inline_keyboard=[
#                 [InlineKeyboardButton(text='Эпоха', callback_data='fl_epoch'), InlineKeyboardButton(text='Описание', callback_data='fl_about'), InlineKeyboardButton(text='✅ Страна', callback_data='fl_country')],
#                 [InlineKeyboardButton(text='🆕 Сбросить фильтры', callback_data='fl_reset')]
#             ]
#         )
    
#     elif about:
#         filter_kb = InlineKeyboardMarkup(
#             inline_keyboard=[
#                 [InlineKeyboardButton(text='Эпоха', callback_data='fl_epoch'), InlineKeyboardButton(text='✅ Описание', callback_data='fl_about'), InlineKeyboardButton(text='Страна', callback_data='fl_country')],
#                 [InlineKeyboardButton(text='🆕 Сбросить фильтры', callback_data='fl_reset')]
#             ]
#         )

#     elif era and country:
#         filter_kb = InlineKeyboardMarkup(
#             inline_keyboard=[
#                 [InlineKeyboardButton(text='✅ Эпоха', callback_data='fl_epoch'), InlineKeyboardButton(text='Описание', callback_data='fl_about'), InlineKeyboardButton(text='✅ Страна', callback_data='fl_country')],
#                 [InlineKeyboardButton(text='🆕 Сбросить фильтры', callback_data='fl_reset')]
#             ]
#         )
    
#     elif era and about:
#         filter_kb = InlineKeyboardMarkup(
#             inline_keyboard=[
#                 [InlineKeyboardButton(text='✅ Эпоха', callback_data='fl_epoch'), InlineKeyboardButton(text='✅ Описание', callback_data='fl_about'), InlineKeyboardButton(text='Страна', callback_data='fl_country')],
#                 [InlineKeyboardButton(text='🆕 Сбросить фильтры', callback_data='fl_reset')]
#             ]
#         )
    
#     elif country and about:
#         filter_kb = InlineKeyboardMarkup(
#             inline_keyboard=[
#                 [InlineKeyboardButton(text='Эпоха', callback_data='fl_epoch'), InlineKeyboardButton(text='✅ Описание', callback_data='fl_about'), InlineKeyboardButton(text='✅ Страна', callback_data='fl_country')],
#                 [InlineKeyboardButton(text='🆕 Сбросить фильтры', callback_data='fl_reset')]
#             ]
#         )
    
#     elif era and country and about:
#         filter_kb = InlineKeyboardMarkup(
#             inline_keyboard=[
#                 [InlineKeyboardButton(text='✅ Эпоха', callback_data='fl_epoch'), InlineKeyboardButton(text='✅ Описание', callback_data='fl_about'), InlineKeyboardButton(text='✅ Страна', callback_data='fl_country')],
#                 [InlineKeyboardButton(text='🆕 Сбросить фильтры', callback_data='fl_reset')]
#             ]
#         )
    
#     return filter_kb