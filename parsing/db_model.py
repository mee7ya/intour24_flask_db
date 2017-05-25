from peewee import *
from peewee import create_model_tables
from playhouse.sqlite_ext import SqliteDatabase

DATABASE = 'tours.db'
database = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = database


class Tour(BaseModel):
    title = CharField()
    date = CharField()
    price = CharField()
    time = CharField()


def migrate():
    create_model_tables([Tour], fail_silently=True)
