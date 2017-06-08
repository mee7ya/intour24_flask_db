from peewee import *
from peewee import create_model_tables
from playhouse.sqlite_ext import SqliteDatabase
import settings as s

DATABASE = s.LOCAL_DB_PATH
database = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = database


class Price(BaseModel):
    price_for_adult = CharField()
    price_for_children = CharField()
    price_for_enfant = CharField()

    @staticmethod
    def get_price_id(price_for_adult, price_for_children, price_for_enfant):
        price = Price()
        price.price_for_adult = price_for_adult
        price.price_for_children = price_for_children
        price.price_for_enfant = price_for_enfant
        price.save()
        return price.id


class PickingPlace(BaseModel):
    name = CharField()
    geoposition = CharField()

    @staticmethod
    def get_place_id(name, geoposition):
        picking_place = PickingPlace()
        picking_place.name = name
        picking_place.geoposition = geoposition
        picking_place.save()
        return picking_place.id


class Tour(BaseModel):
    title = CharField()
    price = ForeignKeyField(Price, null=True)
    duration = CharField(null=True)
    description = CharField(null=True)
    start_point = ForeignKeyField(PickingPlace, null=True)
    photo = CharField()

    def __repr__(self):
        return str(self.title) + " " + str(self.price) + " " + str(self.date) \
               + " " + str(self.duration) + " " + str(self.description) \
               + " " + str(self.start_point) + " " + str(self.photo)


class Dates(BaseModel):
    start_date = CharField()
    repeat_interval = CharField()
    excursion_id = ForeignKeyField(Tour)

    @staticmethod
    def get_dates_id(start_date, repeat_interval):
        dates = Dates()
        dates.start_date = start_date
        dates.repeat_interval = repeat_interval
        dates.save()
        return dates.id


def migrate():
    create_model_tables([Dates, PickingPlace, Price, Tour], fail_silently=True)
