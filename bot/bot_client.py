import os
from balethon import Client
from balethon.conditions import private
from bot_config import Settings
from handlers.message_handler import question_handler
from handlers.start_handler import start_handler
from handlers.callback_handler import question_callback_handler
from handlers.admin_handler import add_student_handler


def create_bot():

    ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))

    if not ADMIN_CHAT_ID:
        return

    print(f"Admin chat id configured: {ADMIN_CHAT_ID}")

    bot = Client(
        token=Settings.BOT_TOKEN
    )

    # start command
    bot.on_command(private, name="start")(start_handler)

    # admin
    # bot.on_command(private, name="addstudent")(add_student_handler)

    # text messages
    bot.on_message()(question_handler)

    # callback
    bot.on_callback_query()(question_callback_handler)

    return bot
