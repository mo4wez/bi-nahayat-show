from datetime import datetime
from peewee import *
from playhouse.sqlite_ext import SqliteDatabase
import os


bot_db = SqliteDatabase(os.getenv("BOT_DB_NAME", "bot/bot_storage.sqlite3"))


class BotBaseModel(Model):
    class Meta:
        database = bot_db


class AllowedStudent(BotBaseModel):
    id = AutoField()
    student_id = CharField(max_length=20, unique=True, index=True)
    full_name = CharField(max_length=150, null=True)
    is_active = BooleanField(default=True)
    added_by_chat_id = BigIntegerField(null=True)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "allowed_students"


class BotUser(BotBaseModel):
    id = AutoField()

    chat_id = BigIntegerField(unique=True, index=True)
    user_id = BigIntegerField(null=True, index=True)

    username = CharField(max_length=150, null=True)
    first_name = CharField(max_length=150, null=True)
    last_name = CharField(max_length=150, null=True)

    student = ForeignKeyField(
        AllowedStudent,
        backref="bot_users",
        null=True,
        on_delete="SET NULL"
    )

    is_verified = BooleanField(default=False)
    is_active = BooleanField(default=True)
    is_admin = BooleanField(default=False)

    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "bot_users"


def init_bot_storage():
    bot_db.connect(reuse_if_open=True)
    bot_db.create_tables([AllowedStudent, BotUser])
