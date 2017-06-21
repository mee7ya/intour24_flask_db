# coding: utf-8
from sqlalchemy import VARCHAR, ARRAY, Boolean, CheckConstraint, Column, DateTime, Float, ForeignKey, Integer, SmallInteger, String, Text, UniqueConstraint
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class AuthGroup(db.Model):
    __tablename__ = 'auth_group'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(80), nullable=False, unique=True)


class AuthGroupPermission(db.Model):
    __tablename__ = 'auth_group_permissions'
    __table_args__ = (
        db.UniqueConstraint('group_id', 'permission_id'),
    )

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    group_id = db.Column(db.ForeignKey('auth_group.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    permission_id = db.Column(db.ForeignKey('auth_permission.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    group = db.relationship('AuthGroup', primaryjoin='AuthGroupPermission.group_id == AuthGroup.id', backref='auth_group_permissions')
    permission = db.relationship('AuthPermission', primaryjoin='AuthGroupPermission.permission_id == AuthPermission.id', backref='auth_group_permissions')


class AuthPermission(db.Model):
    __tablename__ = 'auth_permission'
    __table_args__ = (
        db.UniqueConstraint('content_type_id', 'codename'),
    )

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(255), nullable=False)
    content_type_id = db.Column(db.ForeignKey('django_content_type.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    codename = db.Column(db.String(100), nullable=False)

    content_type = db.relationship('DjangoContentType', primaryjoin='AuthPermission.content_type_id == DjangoContentType.id', backref='auth_permissions')


class AuthUser(db.Model):
    __tablename__ = 'auth_user'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    password = db.Column(db.String(128), nullable=False)
    last_login = db.Column(db.DateTime(True))
    is_superuser = db.Column(db.Boolean, nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    is_staff = db.Column(db.Boolean, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    date_joined = db.Column(db.DateTime(True), nullable=False)


class AuthUserGroup(db.Model):
    __tablename__ = 'auth_user_groups'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'group_id'),
    )

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    user_id = db.Column(db.ForeignKey('auth_user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    group_id = db.Column(db.ForeignKey('auth_group.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    group = db.relationship('AuthGroup', primaryjoin='AuthUserGroup.group_id == AuthGroup.id', backref='auth_user_groups')
    user = db.relationship('AuthUser', primaryjoin='AuthUserGroup.user_id == AuthUser.id', backref='auth_user_groups')


class AuthUserUserPermission(db.Model):
    __tablename__ = 'auth_user_user_permissions'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'permission_id'),
    )

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    user_id = db.Column(db.ForeignKey('auth_user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    permission_id = db.Column(db.ForeignKey('auth_permission.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    permission = db.relationship('AuthPermission', primaryjoin='AuthUserUserPermission.permission_id == AuthPermission.id', backref='auth_user_user_permissions')
    user = db.relationship('AuthUser', primaryjoin='AuthUserUserPermission.user_id == AuthUser.id', backref='auth_user_user_permissions')


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    tourist_id = db.Column(db.ForeignKey('tourists.id'))
    group_id = db.Column(db.ForeignKey('groups.id'))
    adults = db.Column(db.Integer)
    children = db.Column(db.Integer)
    enfants = db.Column(db.Integer)
    total_price = db.Column(db.Integer)
    create_datetime = db.Column(db.DateTime(True))
    update_datetime = db.Column(db.DateTime(True))
    is_cancelled = db.Column(db.Integer)

    group = db.relationship('Group', primaryjoin='Booking.group_id == Group.id', backref='bookings')
    tourist = db.relationship('Tourist', primaryjoin='Booking.tourist_id == Tourist.id', backref='bookings')


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String)
    icon = db.Column(db.String)


class DjangoAdminLog(db.Model):
    __tablename__ = 'django_admin_log'
    __table_args__ = (
        db.CheckConstraint('action_flag >= 0'),
    )

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    action_time = db.Column(db.DateTime(True), nullable=False)
    object_id = db.Column(db.Text)
    object_repr = db.Column(db.String(200), nullable=False)
    action_flag = db.Column(db.SmallInteger, nullable=False)
    change_message = db.Column(db.Text, nullable=False)
    content_type_id = db.Column(db.ForeignKey('django_content_type.id', deferrable=True, initially='DEFERRED'), index=True)
    user_id = db.Column(db.ForeignKey('auth_user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    content_type = db.relationship('DjangoContentType', primaryjoin='DjangoAdminLog.content_type_id == DjangoContentType.id', backref='django_admin_logs')
    user = db.relationship('AuthUser', primaryjoin='DjangoAdminLog.user_id == AuthUser.id', backref='django_admin_logs')


class DjangoContentType(db.Model):
    __tablename__ = 'django_content_type'
    __table_args__ = (
        db.UniqueConstraint('app_label', 'model'),
    )

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    app_label = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)


class DjangoMigration(db.Model):
    __tablename__ = 'django_migrations'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    app = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    applied = db.Column(db.DateTime(True), nullable=False)


class DjangoSession(db.Model):
    __tablename__ = 'django_session'

    session_key = db.Column(db.String(40), primary_key=True, index=True)
    session_data = db.Column(db.Text, nullable=False)
    expire_date = db.Column(db.DateTime(True), nullable=False, index=True)


class ExcursionProperty(db.Model):
    __tablename__ = 'excursion_property'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String)
    icon = db.Column(db.String)


class Excursion(db.Model):
    __tablename__ = 'excursions'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    capacity = db.Column(db.Integer)
    average_rating = db.Column(db.Float)
    duration = db.Column(db.Text)
    category_id = db.Column(db.ForeignKey('category.id'))
    picking_place_id = db.Column(db.ForeignKey('picking_places.id'))
    operator_id = db.Column(db.ForeignKey('operator.id'))
    link_to_site = db.Column(db.String)
    images = db.Column(db.ARRAY(VARCHAR()))
    price_id = db.Column(db.ForeignKey('prices.id'))

    category = db.relationship('Category', primaryjoin='Excursion.category_id == Category.id', backref='excursions')
    operator = db.relationship('Operator', primaryjoin='Excursion.operator_id == Operator.id', backref='excursions')
    picking_place = db.relationship('PickingPlace', primaryjoin='Excursion.picking_place_id == PickingPlace.id', backref='excursions')
    price = db.relationship('Price', primaryjoin='Excursion.price_id == Price.id', backref='excursions')


class ExcursionsExcursionProperty(db.Model):
    __tablename__ = 'excursions_excursion_property'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    excursion_id = db.Column(db.ForeignKey('excursions.id'))
    excursion_property_id = db.Column(db.ForeignKey('excursion_property.id'))

    excursion = db.relationship('Excursion', primaryjoin='ExcursionsExcursionProperty.excursion_id == Excursion.id', backref='excursions_excursion_properties')
    excursion_property = db.relationship('ExcursionProperty', primaryjoin='ExcursionsExcursionProperty.excursion_property_id == ExcursionProperty.id', backref='excursions_excursion_properties')


class ExcursionsSight(db.Model):
    __tablename__ = 'excursions_sights'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    excursion_id = db.Column(db.ForeignKey('excursions.id'))
    sight_id = db.Column(db.ForeignKey('sights.id'))

    excursion = db.relationship('Excursion', primaryjoin='ExcursionsSight.excursion_id == Excursion.id', backref='excursions_sights')
    sight = db.relationship('Sight', primaryjoin='ExcursionsSight.sight_id == Sight.id', backref='excursions_sights')


class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    tour_date = db.Column(db.DateTime(True))
    seats_reserved = db.Column(db.Integer)
    excursion_id = db.Column(db.ForeignKey('excursions.id'))
    guide_id = db.Column(db.ForeignKey('guides.id'))
    seats_capacity = db.Column(db.Integer)

    excursion = db.relationship('Excursion', primaryjoin='Group.excursion_id == Excursion.id', backref='groups')
    guide = db.relationship('Guide', primaryjoin='Group.guide_id == Guide.id', backref='groups')


class Guide(db.Model):
    __tablename__ = 'guides'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    first_name = db.Column(db.String(60))
    email = db.Column(db.String(40))
    phone = db.Column(db.String(20))
    last_name = db.Column(db.String)
    average_rating = db.Column(db.Float)


class Operator(db.Model):
    __tablename__ = 'operator'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String)
    phone = db.Column(db.String)
    address = db.Column(db.String)
    logo = db.Column(db.String)
    accreditation = db.Column(db.Boolean)
    email = db.Column(db.String)


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    booking_id = db.Column(db.ForeignKey('bookings.id'))
    create_datetime = db.Column(db.DateTime(True))
    cancelled_datetime = db.Column(db.DateTime(True))
    refund_datetime = db.Column(db.DateTime(True))
    is_cancelled = db.Column(db.Integer)
    is_refund = db.Column(db.Integer)
    identifier = db.Column(db.String(15))

    booking = db.relationship('Booking', primaryjoin='Payment.booking_id == Booking.id', backref='payments')


class PickingPlace(db.Model):
    __tablename__ = 'picking_places'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(60))
    geoposition = db.Column(db.String(50))


class Price(db.Model):
    __tablename__ = 'prices'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    price_for_children = db.Column(db.Integer)
    price_for_adult = db.Column(db.Integer)
    price_for_enfant = db.Column(db.Integer)


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    excursion_id = db.Column(db.ForeignKey('excursions.id'), db.ForeignKey('excursions.id'))
    guide_id = db.Column(db.ForeignKey('guides.id'))
    excursion_rate = db.Column(db.Integer)
    guide_rate = db.Column(db.Integer)
    feedback = db.Column(db.Text)

    excursion = db.relationship('Excursion', primaryjoin='Review.excursion_id == Excursion.id', backref='excursion_reviews')
    excursion1 = db.relationship('Excursion', primaryjoin='Review.excursion_id == Excursion.id', backref='excursion_reviews_0')
    guide = db.relationship('Guide', primaryjoin='Review.guide_id == Guide.id', backref='reviews')


class Schedule(db.Model):
    __tablename__ = 'schedule'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    start_date = db.Column(db.DateTime(True))
    repeat_interval = db.Column(db.Integer)
    repeat_weekday = db.Column(db.Integer)
    repeat_week = db.Column(db.Integer)
    end_date = db.Column(db.DateTime(True))
    excursion_id = db.Column(db.ForeignKey('excursions.id'), nullable=False)
    repeat_year = db.Column(db.Integer)
    repeat_month = db.Column(db.Integer)
    repeat_day = db.Column(db.Integer)

    excursion = db.relationship('Excursion', primaryjoin='Schedule.excursion_id == Excursion.id', backref='schedules')


class SightProperty(db.Model):
    __tablename__ = 'sight_property'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String)
    image = db.Column(db.String)


class Sight(db.Model):
    __tablename__ = 'sights'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(60))
    geoposition = db.Column(db.String(50))
    images = db.Column(db.ARRAY(db.VARCHAR(length=70)))
    description = db.Column(db.Text)
    cover = db.Column(db.String)


class SightsSightProperty(db.Model):
    __tablename__ = 'sights_sight_property'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    sight_id = db.Column(db.ForeignKey('sights.id'))
    sight_property_id = db.Column(db.ForeignKey('sight_property.id'))

    sight = db.relationship('Sight', primaryjoin='SightsSightProperty.sight_id == Sight.id', backref='sights_sight_properties')
    sight_property = db.relationship('SightProperty', primaryjoin='SightsSightProperty.sight_property_id == SightProperty.id', backref='sights_sight_properties')


class Tourist(db.Model):
    __tablename__ = 'tourists'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    first_name = db.Column(db.String(60))
    email = db.Column(db.String(40))
    phone = db.Column(db.String(20))
    last_name = db.Column(db.String)


class Transport(db.Model):
    __tablename__ = 'transport'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    capacity = db.Column(db.Integer)
    number = db.Column(db.String)
    group_id = db.Column(db.ForeignKey('groups.id'))

    group = db.relationship('Group', primaryjoin='Transport.group_id == Group.id', backref='transports')


class TransportType(db.Model):
    __tablename__ = 'transport_type'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String)
    transport_id = db.Column(db.ForeignKey('transport.id'))

    transport = db.relationship('Transport', primaryjoin='TransportType.transport_id == Transport.id', backref='transport_types')
