from services.user_service import UserService


async def add_student_handler(*, message):
    UserService.upsert_user_from_message(message)

    chat_id = message.chat.id
    text = (message.text or "").strip()

    print(f"text in add_student_handler: {text}")

    if not UserService.is_admin(int(chat_id)):
        await message.reply("شما دسترسی ادمین ندارید.")
        return

    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("فرمت درست:\n/addstudent 40111812365")
        return

    student_id = parts[1].strip()

    if not UserService.is_valid_student_id(student_id):
        await message.reply("کد دانشجویی نامعتبر است. باید 11 رقم و فقط عدد باشد.")
        return

    student = UserService.add_allowed_student(
        student_id=student_id,
        added_by_chat_id=chat_id,
    )

    await message.reply(f"کد دانشجویی {student.student_id} با موفقیت ثبت شد.")
