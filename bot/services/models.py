# services/models.py

from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase
from playhouse.sqlite_ext import SqliteDatabase
import os

# -------------------------------------------------------------------
# DATABASE CONFIG
# -------------------------------------------------------------------

DB_ENGINE = os.getenv("DB_ENGINE", "sqlite")  # sqlite or postgres

if DB_ENGINE == "postgres":
    db = PostgresqlExtDatabase(
        os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 5432)),
    )
else:
    db = SqliteDatabase(os.getenv("DB_NAME", "db.sqlite3"))


# -------------------------------------------------------------------
# BASE MODEL
# -------------------------------------------------------------------

class BaseModel(Model):
    class Meta:
        database = db


# -------------------------------------------------------------------
# STEP MODEL
# -------------------------------------------------------------------

class Step(BaseModel):
    id = AutoField()  # Django default PK

    step_number = IntegerField(unique=True)
    title = CharField(max_length=200)
    description = TextField(null=True)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = "courses_step"   # ✅ CHANGE if your app name differs


# -------------------------------------------------------------------
# LEVEL MODEL
# -------------------------------------------------------------------

class Level(BaseModel):
    id = AutoField()

    step = ForeignKeyField(
        Step,
        backref="levels",
        column_name="step_id",
        on_delete="CASCADE"
    )

    level_number = IntegerField()
    title = CharField(max_length=200)
    description = TextField(null=True)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = "courses_level"
        indexes = (
            (("step", "level_number"), True),
        )


# -------------------------------------------------------------------
# QUESTION MODEL
# -------------------------------------------------------------------

class Question(BaseModel):
    id = AutoField()

    level = ForeignKeyField(
        Level,
        backref="questions",
        column_name="level_id",
        on_delete="CASCADE"
    )

    question_number = IntegerField()
    question_text = TextField()
    answer = TextField()
    hint = TextField(null=True)
    tags = CharField(max_length=500, null=True)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = "courses_question"
        indexes = (
            (("level", "question_number"), True),
        )
