# utils/formatter.py

def truncate_text(text: str, max_length: int = 40):
    """کوتاه کردن متن برای نمایش در دکمه‌های کیبورد"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def format_question_result(question):
    """فرمت‌ بندی نهایی برای نمایش به کاربر"""
    return (
        f"📘 *{question.level.step.title}* - {question.level.title}\n"
        f"❓ *سوال {question.question_number}:*\n"
        f"{question.question_text}\n\n"
        f"✅ *پاسخ:*\n"
        f"{question.answer}\n\n"
        f"💡 نکته:\n"
        f"{question.hint if question.hint else 'نکته ای ثبت نشده'}\n\n"
        f"🏷 # {' #'.join(question.tags.split(',')) if question.tags else 'هیچ تگی ثبت نشده'}"
    )
