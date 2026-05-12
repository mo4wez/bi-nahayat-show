# handlers/callback_handler.py

from services.models import Question
from utils.formatter import format_question_result
from constants.keyboards import build_back_keyboard, build_question_results_keyboard
from services.search_service import SearchService
from services.user_service import UserService

async def question_callback_handler(*, callback_query):
    chat_id = callback_query.message.chat.id
    UserService.upsert_user_from_message(callback_query.message)

    if not UserService.is_verified(chat_id):
        await callback_query.answer("ابتدا احراز هویت کنید.", show_alert=True)
        return

    data = callback_query.data or ""

    # حالت پاسخ به یک سوال خاص
    if data.startswith("q:"):
        _, q_id, search_query = data.split(":", 2)

        question = Question.get_by_id(int(q_id))
        text = format_question_result(question)

        keyboard = build_back_keyboard(search_query)

        await callback_query.message.edit(
            text,
            reply_markup=keyboard
        )

        await callback_query.answer()
        return

    # حالت بازگشت
    if data.startswith("back:"):
        query = data.split(":", 1)[1]

        results = SearchService.search_optimized(query)
        keyboard = build_question_results_keyboard(results, search_query=query)

        await callback_query.message.edit(
            "🔎 Results:",
            reply_markup=keyboard
        )

        await callback_query.answer()
        return
