from bot_client import create_bot
from services.models import db
from services.storage_models import bot_db, init_bot_storage
from peewee import OperationalError


def main():

    if db.is_closed() and bot_db.is_closed():
        db.connect()
        try:
            init_bot_storage()
        except OperationalError as e:
            print(e)


    bot = create_bot()

    bot.run()


if __name__ == "__main__":
    main()
