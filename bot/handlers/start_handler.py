import os
from services.user_service import UserService
from services.auth_state import set_waiting_for_student_id

ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))
ADMIN_STUDENT_ID = str(os.getenv("ADMIN_STUDENT_ID", "0"))

async def start_handler(*, message):
    print(f"message:\n{message}")
    user = UserService.upsert_user_from_message(message)
    chat_id = message.chat.id

    if chat_id == ADMIN_CHAT_ID:
        UserService.set_admin(chat_id, True)
        UserService.verify_user(chat_id, ADMIN_STUDENT_ID)
        user = UserService.get_by_chat_id(chat_id)

    if user and user.is_verified:
        await message.reply("سلام. خوش آمدید. شما قبلاً احراز هویت شده‌اید و می‌توانید از ربات استفاده کنید.")
        return

    set_waiting_for_student_id(chat_id)
    await message.reply(
        "سلام.\n"
        "برای استفاده از ربات، لطفاً کد دانشجویی 11 رقمی خود را ارسال کنید."
    )

