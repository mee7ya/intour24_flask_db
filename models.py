# coding: utf-8
from sqlalchemy import ARRAY, Boolean, Column, Date, Float, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Excursion(Base):
    __tablename__ = 'excursions'

    id = Column(Integer, primary_key=True, server_default=text("nextval('excursions_id_seq'::regclass)"))
    name = Column(String(200))
    description = Column(Text)
    price = Column(Integer)
    capacity = Column(Integer)
    is_picking = Column(Boolean)
    default_picking_place = Column(String(100))
    schedule = Column(Text)
    average_rating = Column(Float)
    duration = Column(Text)


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    tour_date = Column(Date)
    reserved = Column(Integer)
    picking_place = Column(ForeignKey('picking_places.id'))
    excursion = Column(ForeignKey('excursions.id'))
    tourist = Column(ForeignKey('tourists.id'))
    guide = Column(ForeignKey('guides.id'))
    tour_time = Column(ARRAY(TIME()))

    excursion1 = relationship('Excursion')
    guide1 = relationship('Guide')
    picking_place1 = relationship('PickingPlace')
    tourist1 = relationship('Tourist', primaryjoin='Group.tourist == Tourist.id')


class Guide(Base):
    __tablename__ = 'guides'

    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    email = Column(String(40))
    phone_number = Column(String(20))
    average_rating = Column(Float(53))


class PickingPlace(Base):
    __tablename__ = 'picking_places'

    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    geoposition = Column(String(50))


class Place(Base):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    geoposition = Column(String(50))


class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True)
    excursion = Column(ForeignKey('excursions.id'))
    guide = Column(ForeignKey('guides.id'))
    excursion_rate = Column(Integer)
    guide_rate = Column(Integer)
    feedback = Column(Text)

    excursion1 = relationship('Excursion')
    guide1 = relationship('Guide')


class Tourist(Base):
    __tablename__ = 'tourists'

    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    email = Column(String(40))
    hotel_number = Column(Integer)
    phone_number = Column(String(20))
    picking_place = Column(ForeignKey('picking_places.id'))
    group = Column(ForeignKey('groups.id'))

    group1 = relationship('Group', primaryjoin='Tourist.group == Group.id')
    picking_place1 = relationship('PickingPlace')
