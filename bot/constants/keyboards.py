# constants/keyboards.py

from balethon.objects import InlineKeyboard, InlineKeyboardButton
from utils.formatter import truncate_text

def build_question_results_keyboard(questions, search_query=None):
    keyboard = InlineKeyboard()
    keyboard.inline_keyboard = []

    for index, q in enumerate(questions):
        summary = truncate_text(q.question_text, 45)

        callback = f"q:{q.id}:{search_query or ''}"

        button = InlineKeyboardButton(text=f"❓ {summary}", callback_data=callback)

        keyboard.inline_keyboard.append([button])
    
    return keyboard


def build_back_keyboard(search_query: str):
    keyboard = InlineKeyboard()
    keyboard.inline_keyboard = []

    callback = f"back:{search_query}"

    button = InlineKeyboardButton(
        text="🔙 Back to results",
        callback_data=callback
    )

    keyboard.inline_keyboard.append([button])


    return keyboard

