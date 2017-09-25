from peewee import *
from peewee import create_model_tables
from playhouse.sqlite_ext import SqliteDatabase
import settings as s

DATABASE = s.LOCAL_DB_PATH
database = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = database


class Sight(BaseModel):
    name = CharField(null=True)
    image = CharField(null=True)


class ExcursionProperty(BaseModel):
    name = CharField(null=True)
    image = CharField(null=True)


class Price(BaseModel):
    price_for_adult = CharField()
    price_for_children = CharField()

    # price_for_enfant = CharField()

    @staticmethod
    def get_price_id(price_for_adult, price_for_children):  # price_for_enfant):
        price = Price()
        price.price_for_adult = price_for_adult
        price.price_for_children = price_for_children
        # price.price_for_enfant = price_for_enfant
        price.save()
        return price.id


class PickingPlace(BaseModel):
    name = CharField()

    @staticmethod
    def get_place_id(name):
        picking_place = PickingPlace()
        picking_place.name = name
        picking_place.save()
        return picking_place.id


class Excursion(BaseModel):
    name = CharField(null=True)
    description = CharField(null=True)
    duration = CharField(null=True)
    picking_place = ForeignKeyField(PickingPlace, null=True)
    price = ForeignKeyField(Price, null=True)

    def __repr__(self):
        return str(self.name) + " " + str(self.description) + " " + str(self.duration) \
               + " " + str(self.picking_place) + " " + str(self.price)


class Schedule(BaseModel):
    excursion = ForeignKeyField(Excursion, null=True)
    start_date = DateField(null=True)
    end_date = DateField(null=True)
    start_time = TimeField(null=True)
    everyday = IntegerField(null=True)
    weekday = IntegerField(null=True)
    odd_even_week = IntegerField(null=True)
    repeat_day = IntegerField(null=True)


def migrate():
    create_model_tables([Schedule, PickingPlace, Price, Excursion, Sight, ExcursionProperty], fail_silently=True)
