from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура выбора стиля
mode_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Ordinary"), KeyboardButton(text="Friendly")],
        [KeyboardButton(text="Professional")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Select translation style..."
)

# Клавиатура выбора языка
lang_kb = ReplyKeyboardMarkup(
    keyboard=[
        # Первый ряд кнопок
        [KeyboardButton(text="🇷🇺 To Russian"), KeyboardButton(text="🇺🇸 To English")],
        [KeyboardButton(text="🔙 Back to Style")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Select language..."
)

# Главное меню (когда бот уже в режиме перевода)
main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔄 Change Language"), KeyboardButton(text="🎭 Change Style")],
        [KeyboardButton(text="🛑 Restart / Reset")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Send text to translate..."
)