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

    def __repr__(self):
        return str(self.title) + " " + str(self.price) + " " + str(self.date) + " " + str(self.time)


def migrate():
    create_model_tables([Tour], fail_silently=True)
