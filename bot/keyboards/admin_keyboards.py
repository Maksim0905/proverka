from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                            ReplyKeyboardMarkup, KeyboardButton)


reuests = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🌐 Заявки', callback_data='requests')]
    ]
)