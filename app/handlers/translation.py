from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.services.llm_engine import get_translation
from app.states import TranslationStates
from app.keyboards import mode_kb, lang_kb, main_menu_kb

router = Router()

# 1. Старт
@router.message(Command("start"))
@router.message(F.text == "🛑 Restart / Reset")
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Welcome! Let's translate.\nFirst, choose **Style**:",
        reply_markup=mode_kb
    )
    await state.set_state(TranslationStates.choosing_mode)


# 2. Выбор стиля
@router.message(TranslationStates.choosing_mode)
async def style_chosen(message: Message, state: FSMContext):
    
    allowed_styles = ["ordinary", "friendly", "professional"]
    
    if message.text.lower() not in allowed_styles:
        await message.answer(
            "⛔️ Please select a style using the buttons below:", 
            reply_markup=mode_kb
        )
        return

    await state.update_data(mode=message.text.lower())
    await message.answer(
        f"✅ Style: **{message.text}**.\nNow choose **Target Language**:",
        reply_markup=lang_kb
    )
    await state.set_state(TranslationStates.choosing_language)


# 3. Выбор языка
@router.message(TranslationStates.choosing_language)
async def language_chosen(message: Message, state: FSMContext):
    text = message.text
    
    if text == "🔙 Back to Style":
        await message.answer("Okay, choose style:", reply_markup=mode_kb)
        await state.set_state(TranslationStates.choosing_mode)
        return

    # Проверяем, нажал ли пользователь кнопку или написал ерунду
    # Разрешаем только если текст содержит ключевые слова из кнопок
    valid_langs = ["Russian", "English"]
    is_valid = False
    target_lang = "English"

    if "Russian" in text:
        target_lang = "Russian"
        is_valid = True
    elif "English" in text:
        target_lang = "English"
        is_valid = True

    if not is_valid:
        await message.answer(
            "⛔️ Please choose a language using the buttons!", 
            reply_markup=lang_kb
        )
        return

    await state.update_data(target_lang=target_lang)
    data = await state.get_data()
    mode = data.get("mode", "ordinary")
    
    await message.answer(
        f"🎉 **Ready!**\nStyle: {mode.capitalize()} | Target: {target_lang}\n\n"
        "👇 Send text to translate:",
        reply_markup=main_menu_kb
    )
    await state.set_state(TranslationStates.translating)


# 4. Кнопки смены настроек
@router.message(TranslationStates.translating, F.text == "🔄 Change Language")
async def change_lang_btn(message: Message, state: FSMContext):
    await message.answer("Select new language:", reply_markup=lang_kb)
    await state.set_state(TranslationStates.choosing_language)

@router.message(TranslationStates.translating, F.text == "🎭 Change Style")
async def change_style_btn(message: Message, state: FSMContext):
    await message.answer("Select new style:", reply_markup=mode_kb)
    await state.set_state(TranslationStates.choosing_mode)


# 4.1 Блокировка медиа во всех состояниях
@router.message(F.photo)
async def handle_photo(message: Message, state: FSMContext):
    await message.answer("📷 I can only translate text. Send me text to translate.")

@router.message(F.video)
async def handle_video(message: Message, state: FSMContext):
    await message.answer("🎬 I can only translate text. Send me text to translate.")

@router.message(F.sticker)
async def handle_sticker(message: Message, state: FSMContext):
    await message.answer("😎 I can only translate text. Send me text to translate.")

@router.message(F.document)
async def handle_document(message: Message, state: FSMContext):
    await message.answer("📄 I can only translate text. Send me text to translate.")

@router.message(F.voice)
async def handle_voice(message: Message, state: FSMContext):
    await message.answer("🎤 I can only translate text. Send me text to translate.")


# 5. Перевод (только текст)
@router.message(TranslationStates.translating, F.text)
async def handle_translation(message: Message, state: FSMContext):
    data = await state.get_data()
    mode = data.get("mode", "ordinary")
    target_lang = data.get("target_lang", "English")
    
    wait_msg = await message.answer("⏳ Translating...")
    translation = await get_translation(message.text, mode, target_lang)
    
    await wait_msg.delete()
    await message.answer(translation, reply_markup=main_menu_kb)