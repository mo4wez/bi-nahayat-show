# bot/config.py

"""
Advanced configuration module for the bot.
Supports multi-environment setup and validation.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


# ---------------------------------------------------
# LOAD ENV FILE
# ---------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)


# ---------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------

def get_env(key: str, default=None, required: bool = False):
    value = os.getenv(key, default)

    if required and value is None:
        raise RuntimeError(f"Missing required environment variable: {key}")

    return value


def get_bool(key: str, default: bool = False) -> bool:
    return str(os.getenv(key, default)).lower() in ("true", "1", "yes")


def get_int(key: str, default: int) -> int:
    return int(os.getenv(key, default))


# ---------------------------------------------------
# CORE SETTINGS
# ---------------------------------------------------

class Settings:
    """
    Central configuration class.
    All settings are accessed through this object.
    """

    # ---------- Environment ----------
    ENV = get_env("ENV", "development")
    DEBUG = get_bool("DEBUG", True)

    # ---------- Bot ----------
    BOT_TOKEN = get_env("BOT_TOKEN", required=True)

    # ---------- Database ----------
    DB_ENGINE = get_env("DB_ENGINE", "sqlite")

    if DB_ENGINE == "sqlite":
        DB_NAME = get_env("DB_NAME", str(BASE_DIR / "db.sqlite3"))
        DB_PATH = BASE_DIR / DB_NAME
    else:
        DB_NAME = get_env("DB_NAME", required=True)
        DB_USER = get_env("DB_USER", required=True)
        DB_PASSWORD = get_env("DB_PASSWORD", required=True)
        DB_HOST = get_env("DB_HOST", "localhost")
        DB_PORT = get_int("DB_PORT", 5432)

    # ---------- Search ----------
    SEARCH_THRESHOLD = get_int("SEARCH_THRESHOLD", 8)
    MAX_SEARCH_RESULTS = get_int("MAX_SEARCH_RESULTS", 10)
    PREVIEW_LENGTH = get_int("PREVIEW_LENGTH", 70)


# Singleton instance
settings = Settings()
