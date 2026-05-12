from services.user_service import UserService
from services.auth_state import (
    is_waiting_for_student_id,
    clear_waiting_for_student_id,
    set_waiting_for_student_id,
)
from services.search_service import SearchService
from constants.keyboards import build_question_results_keyboard
from handlers.admin_handler import add_student_handler
from handlers.start_handler import start_handler
from utils.formatter import format_question_result


async def question_handler(*, message):
    print(f"message:\n {message}")

    text = (message.text or "").strip()
    chat_id = message.chat.id

    if text.startswith("/addstudent"):
        await add_student_handler(message=message)
        return
    
    if text.startswith("/start"):
        await start_handler(message=message)
        return

    if text.startswith("/"):
        return
    
    UserService.upsert_user_from_message(message)

    if is_waiting_for_student_id(chat_id):
        if not UserService.is_valid_student_id(text):
            await message.reply("کد دانشجویی نامعتبر است. لطفاً یک کد 11 رقمی عددی ارسال کنید.")
            return

        success, result_message = UserService.verify_user(int(chat_id), student_id=text)

        if success:
            clear_waiting_for_student_id(chat_id)
            await message.reply(
                result_message + "\nاکنون می‌توانید سوال خود را ارسال کنید."
            )
        else:
            set_waiting_for_student_id(chat_id)
            await message.reply(result_message)

        return

    if not UserService.is_verified(chat_id):
        set_waiting_for_student_id(chat_id)
        await message.reply(
            "برای استفاده از ربات ابتدا باید احراز هویت شوید.\n"
            "لطفاً کد دانشجویی 11 رقمی خود را ارسال کنید."
        )
        return

    results = SearchService.search_optimized(text)

    if not results:
        await message.reply("نتیجه‌ای پیدا نشد.")
        return

    if len(results) == 1:
        q = results[0]
        await message.reply(format_question_result(q))
        return

    keyboard = build_question_results_keyboard(results, text)
    await message.reply(
        "چند نتیجه پیدا شد. یکی را انتخاب کنید:",
        reply_markup=keyboard
    )
