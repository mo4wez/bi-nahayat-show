from datetime import datetime
from peewee import IntegrityError
from services.storage_models import BotUser, AllowedStudent


class UserService:
    STUDENT_ID_LENGTH = 11

    @staticmethod
    def normalize_student_id(text: str) -> str:
        return (text or "").strip()

    @classmethod
    def is_valid_student_id(cls, text: str) -> bool:
        text = cls.normalize_student_id(text)
        return text.isdigit() and len(text) == cls.STUDENT_ID_LENGTH

    @staticmethod
    def upsert_user_from_message(message):
        now = datetime.now()

        from_user = getattr(message, "author", None)
        chat = getattr(message, "chat", None)

        if not chat:
            return None

        chat_id = getattr(chat, "id", None)
        if chat_id is None:
            return None

        user_id = getattr(from_user, "id", None) if from_user else None
        username = getattr(from_user, "username", None) if from_user else None
        first_name = getattr(from_user, "first_name", None) if from_user else None
        last_name = getattr(from_user, "last_name", None) if from_user else None

        BotUser.insert(
            chat_id=chat_id,
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            created_at=now,
            updated_at=now,
        ).on_conflict(
            conflict_target=[BotUser.chat_id],
            preserve=[BotUser.created_at],
            update={
                BotUser.user_id: user_id,
                BotUser.username: username,
                BotUser.first_name: first_name,
                BotUser.last_name: last_name,
                BotUser.updated_at: now,
            }
        ).execute()

        return BotUser.get_or_none(BotUser.chat_id == chat_id)

    @staticmethod
    def get_by_chat_id(chat_id: int):
        return BotUser.get_or_none(BotUser.chat_id == chat_id)

    @staticmethod
    def is_verified(chat_id: int) -> bool:
        user = BotUser.get_or_none(BotUser.chat_id == chat_id)
        return bool(user and user.is_verified and user.is_active)

    @staticmethod
    def set_admin(chat_id: int, is_admin: bool = True):
        user = BotUser.get_or_none(BotUser.chat_id == chat_id)
        if not user:
            return None
        user.is_admin = is_admin
        user.updated_at = datetime.now()
        user.save()
        return user

    @staticmethod
    def is_admin(chat_id: int) -> bool:
        user = BotUser.get_or_none(BotUser.chat_id == chat_id)
        return bool(user and user.is_admin and user.is_active)

    @staticmethod
    def add_allowed_student(student_id: str, added_by_chat_id: int = None, full_name: str = None):
        student_id = student_id.strip()

        try:
            return AllowedStudent.create(
                student_id=student_id,
                full_name=full_name,
                added_by_chat_id=added_by_chat_id,
            )
        except IntegrityError:
            return AllowedStudent.get(AllowedStudent.student_id == student_id)

    @staticmethod
    def verify_user(chat_id: int, student_id: str):
        student_id = student_id.strip()

        user = BotUser.get_or_none(BotUser.chat_id == chat_id)
        if not user:
            return False, "کاربر یافت نشد."

        if user.is_verified:
            return False, "شما قبلاً احراز هویت شده‌اید."

        allowed = AllowedStudent.get_or_none(
            (AllowedStudent.student_id == student_id) &
            (AllowedStudent.is_active == True)
        )
        if not allowed:
            return False, "کد دانشجویی شما در لیست مجاز نیست."

        existing_user = BotUser.get_or_none(
            (BotUser.student == allowed) &
            (BotUser.is_verified == True)
        )
        if existing_user and existing_user.chat_id != chat_id:
            return False, "این کد دانشجویی قبلاً استفاده شده است."

        user.student = allowed
        user.is_verified = True
        user.updated_at = datetime.now()
        user.save()

        return True, "احراز هویت شما با موفقیت انجام شد."
