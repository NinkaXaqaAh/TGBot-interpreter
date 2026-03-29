from aiogram.fsm.state import State, StatesGroup

class TranslationStates(StatesGroup):
    choosing_mode = State()      # Этап 1: Выбор стиля (Обычный/Дружелюбный)
    choosing_language = State()  # Этап 2: Выбор языка (Русский/Английский)
    translating = State()        # Этап 3: Режим перевода (бот ждет текст)