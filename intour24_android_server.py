import requests
from flask import Flask, url_for, request, json, Response
import datetime
from datetime import datetime as dt
import intour24_database
import random
import os
from models import *
from flask_sqlalchemy import SQLAlchemy

MEDIA_ROOT="https://intour24.ru/media/"

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://intour24_admin:R9i477o#W7cv@188.130.155.89/intour24_test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
SMS_URL = 'https://sms.ru/sms/'
SMS_API = '1F5F1DF2-3C6B-D268-A754-75F38D147E70'
__directory__ = os.path.dirname(os.path.realpath(__file__))


def send_400_with_error(error):
    json_response = {'status': "ERROR",
                     'error': error}
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response, 400


def id_checker(id):
    if id != '' and id is not None:
        if id.isdigit():
            if int(id) == 0 or int(id) >= 2147483647:
                return 6
            return -1
        else:
            try:
                if int(id) < 0:
                    return 6
            except ValueError:
                return 5
    else:
        return 1


def id_checker_accept_zero(id):
    if id != '' and id is not None:
        if id.isdigit():
            if int(id) >= 2147483647:
                return 6
            return -1
        else:
            try:
                if int(id) < 0:
                    return 6
            except ValueError:
                return 5
    else:
        return 1


def check_date_by_format(format, str_check):
    if str_check != '' and str_check is not None:
        try:
            datetime.datetime.strptime(str_check, format)
        except ValueError:
            return 4
        return -1
    else:
        return 1


def is_valid_phone(phone):
    if phone != '' and phone is not None:
        if phone.isdigit():
            if len(phone) > 20:
                return 6
            return -1
        else:
            return 5
    else:
        return 1

import pytz

# https://stackoverflow.com/questions/33736182/filter-objects-with-a-datetime-range-0000-to-235999-in-django
def date_start_end(date):
    # convert string to datetime
    from_date = dt.strptime(date, '%Y-%m-%d').date()

    if from_date == dt.now().date():
        # combine `from_date` with now
        from_date = dt.combine(from_date, datetime.datetime.now().time())
    else:
        # combine `from_date` with min time value (00:00)
        from_date = dt.combine(from_date, datetime.time.min)

    # combine `from_date` with max time value (23:59:99) to have end date
    to_date = dt.combine(from_date, datetime.time.max)

    timezoneLocal = pytz.timezone('Europe/Moscow')
    utc = pytz.utc
    from_date = utc.localize(from_date).astimezone(timezoneLocal)
    to_date = utc.localize(to_date).astimezone(timezoneLocal)

    print(from_date, to_date)
    return from_date, to_date


def category_in_json(category):
    if category is not None:
        return {'id': category.id,
                'name': category.name,
                'icon': category.icon}
    else:
        return None


def price_in_json(price):
    if price is not None:
        return {'id': price.id,
                'priceForChildren': price.price_for_children,
                'priceForAdult': price.price_for_adult,
                'priceForEnfant': price.price_for_enfant}
    else:
        return None


def picking_place_in_json(picking_place):
    if picking_place is not None:
        return {'id': picking_place.id,
                'name': picking_place.name,
                'geoposition': picking_place.geoposition}
    else:
        return None


def excursion_properties_in_json(properties):
    rez = []
    for property in properties:
        rez.append({'id': property.id,
                    'name': property.name,
                    'icon': property.icon})
    return rez


def operator_in_json(operator):
    if operator is not None:
        return {'id': operator.id,
                'name': operator.name,
                'phone': operator.phone,
                'address': operator.address,
                'logo': operator.logo,
                'accreditation': operator.accreditation,
                'email': operator.email}
    else:
        return None


def excursion_in_json_full(excursion, properties):
    if excursion is not None:
        return {'id': excursion.id,
                'name': excursion.name,
                'description': excursion.description,
                'capacity': excursion.capacity,
                'rating': excursion.average_rating,
                'duration': excursion.duration,
                'category': category_in_json(excursion.category),
                'pickingPlace': picking_place_in_json(excursion.picking_place),
                'operator': operator_in_json(excursion.operator),
                'linkToSite': excursion.link_to_site,
                'images': excursion.images,
                'price': price_in_json(excursion.price),
                'properties': excursion_properties_in_json(properties)}
    else:
        return None


def excursion_in_json_full_with_properties_pars(excursion):
    if excursion is not None:
        id = excursion.id
        properties = db2.session.query(ExcursionProperty). \
            outerjoin(ExcursionsExcursionProperty, ExcursionsExcursionProperty.excursion_id == id). \
            filter(ExcursionProperty.id == ExcursionsExcursionProperty.excursion_property_id). \
            group_by(ExcursionProperty.id). \
            all()
        return {'id': excursion.id,
                'name': excursion.name,
                'description': excursion.description,
                'capacity': excursion.capacity,
                'rating': excursion.average_rating,
                'duration': excursion.duration,
                'category': category_in_json(excursion.category),
                'pickingPlace': picking_place_in_json(excursion.picking_place),
                'operator': operator_in_json(excursion.operator),
                'linkToSite': excursion.link_to_site,
                'images': excursion.images,
                'price': price_in_json(excursion.price),
                'properties': excursion_properties_in_json(properties)}
    else:
        return None


def excursion_in_json_full_with_properties_pars_through_group(group):
    if group is not None:
        return excursion_in_json_full_with_properties_pars(group.excursion)
    else:
        return None


def excursions_in_json(excursions):
    rez = []
    for excursion in excursions:
        rez.append({'id': excursion.id,
                    'name': excursion.name,
                    'description': excursion.description,
                    'capacity': excursion.capacity,
                    'rating': excursion.average_rating,
                    'duration': excursion.duration,
                    'categotyId': excursion.category_id,
                    'startPlaceId': excursion.picking_place_id,
                    'operatorId': excursion.operator_id,
                    'linkToSite': excursion.link_to_site,
                    'images': excursion.images,
                    'priceId': excursion.price_id})
    return rez


def sight_min_max_price(sight):
    prices = []
    excursions_sights = ExcursionsSight.query.filter_by(sight_id=sight.id).all()
    for excursion in excursions_sights:
        excursion = excursion.excursion
        prices.append(excursion.price.price_for_adult)
    if prices:
        min_price = min(prices)
        max_price = max(prices)
    else:
        min_price = None
        max_price = None
    return min_price, max_price


def sight_in_json_full(sight, properties):
    return {'id': sight.id,
            'name': sight.name,
            'geoposition': sight.geoposition,
            'images': sight.images,
            'description': sight.description,
            'cover': MEDIA_ROOT+sight.cover,
            'properties': sight_properties_in_json(properties)}


def sight_properties_in_json(properties):
    rez = []
    for property in properties:
        rez.append({'id': property.id,
                    'name': property.name,
                    'icon': property.icon})
    return rez


def sight_in_json_short(sight):
    return {'id': sight.id,
            'name': sight.name,
            'geoposition': sight.geoposition,
            'images': sight.images,
            'description': sight.description,
            'cover': MEDIA_ROOT+sight.cover}


def guide_in_json(guide):
    if guide is not None:
        return {'id': guide.id,
                'firstName': guide.first_name,
                'email': guide.email,
                'phone': guide.phone,
                'lastName': guide.last_name,
                'rating': guide.average_rating}
    else:
        return None


def groups_with_excursions_in_json_full(groups):
    rez = []
    for group in groups:
        rez.append({'id': group.id,
                    'tourDate': str(group.tour_date),
                    'seatsReserved': group.seats_reserved,
                    'excursion': excursion_in_json_full_with_properties_pars(group.excursion),
                    'guide': guide_in_json(group.guide),
                    'seatsCapacity': group.seats_capacity})
    return rez


def group_with_excursions_in_json_full(group):
    if group is not None:
        return {'id': group.id,
                'tourDate': str(group.tour_date),
                'seatsReserved': group.seats_reserved,
                'excursion': excursion_in_json_full_with_properties_pars(group.excursion),
                'guide': guide_in_json(group.guide),
                'seatsCapacity': group.seats_capacity}
    else:
        return None


def group_in_json_short(group):
    if group is not None:
        return {'id': group.id,
                'tourDate': str(group.tour_date)}


def bookings_in_json(bookings):
    rez = []
    for booking in bookings:
        payment_id = db2.session.query(Payment.id).filter_by(booking_id=booking.id).first()
        if payment_id:
            payment_id = payment_id[0]
        else:
            payment_id = None
        rez.append({'id': booking.id,
                    'touristId': booking.tourist_id,
                    'excursion': excursion_in_json_full_with_properties_pars_through_group(booking.group),
                    'totalPrice': booking.total_price,
                    'paymentId': payment_id,
                    'group': group_in_json_short(booking.group),
                    'isCancelled': booking.is_cancelled,
                    'created': str(booking.create_datetime)})
    return rez


def booking_in_json(booking):
    if booking is not None:
        return {'id': booking.id,
                'adults': booking.adults,
                'children': booking.children,
                'enfants': booking.enfants,
                'totalPrice': booking.total_price,
                'group': group_with_excursions_in_json_full(booking.group),
                'isCancelled': booking.is_cancelled,
                'created': str(booking.create_datetime)}


def payment_in_json_short(payment):
    if payment is not None:
        return {'id': payment.id,
                'bookingId': payment.booking_id,
                'createDatetime': payment.create_datetime,
                'cancelledDatetime': payment.cancelled_datetime,
                'refundDatetime': payment.refund_datetime,
                'isCancelled': payment.is_cancelled,
                'isRefund': payment.is_refund,
                'idenitfier': payment.identifier}


@app.route('/excursion/<id>')
def excursion(id):
    id_code = id_checker(id)
    if id_code != -1:
        return send_400_with_error(id_code)
    excursion = db2.session.query(Excursion).filter_by(id=id).first()
    properties = db2.session.query(ExcursionProperty).\
        outerjoin(ExcursionsExcursionProperty, ExcursionsExcursionProperty.excursion_id == id).\
        filter(ExcursionProperty.id == ExcursionsExcursionProperty.excursion_property_id).\
        group_by(ExcursionProperty.id).\
        all()
    if excursion is None:
        return send_400_with_error(2)
    json_response = excursion_in_json_full(excursion, properties)
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/excursions/')
def excursions():
    excursions = Excursion.query.all()
    json_response = excursions_in_json(excursions)
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/sight/<id>')
def sight(id):
    id_code = id_checker(id)
    if id_code != -1:
        return send_400_with_error(id_code)
    sight = db2.session.query(Sight).filter_by(id=id).first()
    properties = db2.session.query(SightProperty).\
        outerjoin(SightsSightProperty, SightsSightProperty.sight_id == id).\
        filter(SightsSightProperty.sight_property_id == SightProperty.id).\
        group_by(SightProperty.id).\
        all()
    if sight is not None:
        json_response = sight_in_json_full(sight, properties)
        json_response = json.dumps(json_response)
        response = Response(json_response, content_type='application/json; charset=utf-8')
        return response
    else:
        return send_400_with_error(2)


@app.route('/sights/')
def sights():
    sights = Sight.query.order_by(Sight.id).all()
    json_response = []
    for sight in sights:
        min_price, max_price = sight_min_max_price(sight)
        json_sight = sight_in_json_short(sight)
        json_sight['minPrice'] = min_price
        json_sight['maxPrice'] = max_price
        json_response.append(json_sight)
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/groups/', methods=['POST'])
def groups_upd():
    group_id = request.form.get('groupId')
    seats_reserved = request.form.get('seatsReserved')
    group_id_code = id_checker(group_id)
    if group_id_code != -1:
        return send_400_with_error(group_id_code)
    seats_reserved_code = id_checker_accept_zero(seats_reserved)
    if seats_reserved_code != -1:
        send_400_with_error(seats_reserved_code)
    group = db2.session.query(Group).filter_by(id=group_id).first()
    if group is not None:
        more_seats_reserved = int(group.seats_reserved)+int(seats_reserved)
        if more_seats_reserved < 0:
            return send_400_with_error(6)
        if more_seats_reserved <= group.seats_capacity:
            group.seats_reserved = more_seats_reserved
            try:
                db2.session.commit()
            except Exception:
                db2.session.rollback()
            if more_seats_reserved == group.seats_capacity:
                json_response = {'status': "OK",
                                 'full': 1,
                                 'groupId': int(group_id),
                                 'seatsReserved': more_seats_reserved}
            else:
                json_response = {'status': "OK",
                                 'full': 0,
                                 'groupId': int(group_id),
                                 'seatsReserved': more_seats_reserved}
            json_response = json.dumps(json_response)
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response
        else:
            return send_400_with_error(7)
    else:
        return send_400_with_error(2)


@app.route('/groups/<date>/sight/<sight_id>')
def groups(date, sight_id):
    id_code = id_checker(sight_id)
    if id_code != -1:
        return send_400_with_error(id_code)
    date_code = check_date_by_format('%Y-%m-%d', date)
    if date_code != -1:
        return send_400_with_error(date_code)
    date_start, date_end = date_start_end(date)
    sight = db2.session.query(Sight).filter_by(id=sight_id).first()
    excursions = db2.session.query(Excursion).\
        outerjoin(ExcursionsSight, ExcursionsSight.sight_id == sight.id).\
        filter(ExcursionsSight.excursion_id == Excursion.id).\
        group_by(Excursion.id).\
        all()
    groups = []
    for excursion in excursions:
        groups_data = db2.session.query(Group).filter(
            Group.id == excursion.id,
            Group.tour_date > date_start,
            Group.tour_date <= date_end
        ).group_by(Group.id)
        groups.extend(groups_data)
    json_response = json.dumps(groups_with_excursions_in_json_full(groups))
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/group/<id>')
def group(id):
    id_code = id_checker(id)
    if id_code != -1:
        return send_400_with_error(id_code)
    group = db2.session.query(Group).filter_by(id=id).first()
    if group:
        json_response = json.dumps(group_with_excursions_in_json_full(group))
        response = Response(json_response, content_type='application/json; charset=utf-8')
        return response
    else:
        return send_400_with_error(2)


@app.route('/bookings/', methods=['POST'])
def bookings_add():
    group_id = request.form.get('groupId')
    group_id_code = id_checker(group_id)
    if group_id_code != -1:
        return send_400_with_error(group_id_code)
    tourist_id = request.form.get('touristId')
    tourist_id_code = id_checker(tourist_id)
    if tourist_id_code != -1:
        return send_400_with_error(tourist_id_code)
    adults = request.form.get('adults')
    adults_code = id_checker_accept_zero(adults)
    if adults_code != -1:
        return send_400_with_error(adults_code)
    children = request.form.get('children')
    children_code = id_checker_accept_zero(children)
    if children_code != -1:
        return send_400_with_error(children_code)
    enfants = request.form.get('enfants')
    enfants_code = id_checker_accept_zero(enfants)
    if enfants_code != -1:
        return send_400_with_error(enfants_code)
    create_datetime = request.form.get('createDatetime')
    create_datetime_code = check_date_by_format('%Y-%m-%d %H:%M:%S', create_datetime)
    if create_datetime_code != -1:
        return send_400_with_error(create_datetime_code)
    total_price = request.form.get('totalPrice')
    total_price_code = id_checker(total_price)
    if total_price_code != -1:
        return send_400_with_error(total_price_code)
    group = db2.session.query(Group).filter_by(id=group_id).first()
    if group is not None:
        people_reserved = group.seats_reserved + int(children) + int(adults) + int(enfants)
        people_capacity = group.seats_capacity
        if int(people_reserved) <= int(people_capacity):
            booking = Booking()
            booking.tourist_id = tourist_id
            booking.group_id = group_id
            booking.adults = adults
            booking.children = children
            booking.enfants = enfants
            booking.total_price = total_price
            booking.create_datetime = create_datetime
            booking.is_cancelled = 0
            try:
                db2.session.add(booking)
                db2.session.commit()
            except Exception:
                db2.session.rollback()
            if booking.tourist_id is None:
                send_400_with_error(2)
            if people_capacity == people_reserved:
                json_response = {'status': 'OK',
                                 'full': 1,
                                 'id': booking.id,
                                 'created': str(booking.create_datetime)}
                json_response = json.dumps(json_response)
                response = Response(json_response, content_type='application/json; charset=utf-8')
                return response
            else:
                json_response = {'status': 'OK',
                                'full': 0,
                                'id': booking.id,
                                'created': str(booking.create_datetime)}
                json_response = json.dumps(json_response)
                response = Response(json_response, content_type='application/json; charset=utf-8')
                return response
        else:
            return send_400_with_error(7)
    else:
        return send_400_with_error(2)


@app.route('/bookingsByTouristId/<tourist_id>')
def bookings(tourist_id):
    if tourist_id != '0':
        bookings = db2.session.query(Booking).filter_by(tourist_id=tourist_id).all()
        if bookings:
            json_response = json.dumps(bookings_in_json(bookings))
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response
        else:
            json_response = json.dumps([])
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response
    else:
        json_response = json.dumps([])
        response = Response(json_response, content_type='application/json; charset=utf-8')
        return response


@app.route('/booking/<id>')
def booking(id):
        id_code = id_checker(id)
        if id_code != -1:
            return send_400_with_error(id_code)
        booking = db2.session.query(Booking).filter_by(id=id).first()
        if booking is not None:
            json_response = json.dumps(booking_in_json(booking))
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response
        else:
            return send_400_with_error(2)


@app.route('/payments/', methods=['POST'])
def payments_add():
    booking_id = request.form.get('bookingId')
    payment_time = request.form.get('paymentTime')
    identifier = request.form.get('identifier')
    booking_id_code = id_checker(booking_id)
    if booking_id_code != -1:
        return send_400_with_error(booking_id_code)
    payment_time_code = check_date_by_format('%Y-%m-%d %H:%M:%S', payment_time)
    if payment_time_code != -1:
        return send_400_with_error(payment_time_code)
    if identifier == '' or identifier is None:
        return send_400_with_error(1)
    booking = db2.session.query(Booking).filter_by(id=booking_id).first()
    if booking is not None and booking.is_cancelled != 1:
        payment = Payment()
        payment.booking_id = booking_id
        payment.create_datetime = payment_time
        payment.is_cancelled = 0
        payment.is_refund = 0
        payment.identifier = identifier
        try:
            db2.session.add(payment)
            db2.session.commit()
        except Exception:
            db2.session.rollback()
        if payment.id is not None:
            json_response = {'status': "OK",
                             'paymentId': payment.id,
                             'createDatetime': str(payment.create_datetime)}
        else:
            return send_400_with_error(3)
        json_response = json.dumps(json_response)
        response = Response(json_response, content_type='application/json; charset=utf-8')
        return response
    else:
        return send_400_with_error(2)


@app.route('/checkPhone/<phone>')
def check_phone(phone):
    phone_code = is_valid_phone(phone)
    if phone_code != -1:
        return send_400_with_error(phone_code)
    tourist = db2.session.query(Tourist).filter_by(phone=phone).first()
    if tourist is not None:
        code = generate_code()
        if send_sms(code, phone):
            json_response = {"status": "OK",
                         "registered": 1,
                         "id": tourist.id,
                         "code": code}
    else:
        json_response = {"status": "OK",
                         "registered": 0}
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


def generate_code():
    ORDER_NUMBER = 6
    code = str(random.randint(1, 999999))  # ORDER_NUMBER of 999999 = 6
    if len(code) < ORDER_NUMBER:
        code = "0" * (ORDER_NUMBER - len(code)) + code
    return code


def send_sms(code, phone):
    response = requests.get(SMS_URL + 'send?api_id=' + SMS_API + '&to='
                            + phone + '&msg='
                            + code + '&json=1')
    print(code)
    if response.json()['sms'][phone]['status'] == 'OK':
        return True
    else:
        return False


@app.route('/registration', methods=['POST'])
def registration():
    name = request.form.get('name')
    phone = request.form.get('phone')
    phone_code = is_valid_phone(phone)
    if phone_code != -1:
        return send_400_with_error(phone_code)
    if name != '' and name is not None:
        if phone.isdigit():
            tourist = Tourist()
            tourist.first_name = name
            tourist.phone = phone
            try:
                db2.session.add(tourist)
                db2.session.commit()
            except Exception:
                db2.session.rollback()
            if tourist.id is not None:
                code = generate_code()
                send_sms(code, phone)
                json_response = {"status": "OK",
                                 "id": +tourist.id,
                                 "code": code}
            else:
                json_response = {"status": "ERROR",
                                 "error": "2"}
            json_response = json.dumps(json_response)
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response
    return send_400_with_error(1)


@app.route('/updateTourist', methods=['PUT'])
def update_tourist():
    c_id = request.form.get('id')
    name = request.form.get('name')
    phone = request.form.get('phone')
    c_id_code = id_checker(c_id)
    if c_id_code != -1:
        return send_400_with_error(c_id_code)
    phone_code = is_valid_phone(phone)
    if phone_code != -1:
        return send_400_with_error(phone_code)
    if name == '' or name is None:
        return send_400_with_error(1)
    tourist = db2.session.query(Tourist).filter_by(id=c_id).first()
    if tourist.id is not None:
        tourist.first_name = name
        tourist.phone = phone
        try:
            db2.session.commit()
        except Exception:
            db2.session.rollback()
        json_response = {"status": "OK",
                         "id": c_id[0]}
        json_response = json.dumps(json_response)
        response = Response(json_response, content_type='application/json; charset=utf-8')
        return response
    else:
        return send_400_with_error(2)


@app.route('/cancelPayment', methods=['PUT'])
def cancel_payment():
    booking_id = request.form.get('bookingId')
    cancelled_datetime = request.form.get('cancelledDatetime')
    booking_id_code = id_checker(booking_id)
    if booking_id_code != -1:
        return send_400_with_error(booking_id_code)
    cancelled_datetime_code = check_date_by_format('%Y-%m-%d %H:%M:%S', cancelled_datetime)
    if cancelled_datetime_code != -1:
        return send_400_with_error(cancelled_datetime_code)
    payment = db2.session.query(Payment).filter_by(booking_id=booking_id)
    if payment is not None:
        if payment.is_cancelled != 1:
            payment.is_cancelled = 1
            payment.cancelled_datetime = cancelled_datetime
            payment.booking.is_cancelled = 1
            payment.booking.update_datetime = cancelled_datetime
            json_response = {"status": "OK",
                             "paymentId": payment.id,
                             "bookingId": booking.id}
            json_response = json.dumps(json_response)
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response
        else:
            send_400_with_error(2)
    else:
        send_400_with_error(2)


@app.route('/paymentByBookingId/<id>')
def payment_by_booking_id(id):
    id_code = id_checker(id)
    if id_code != -1:
        return send_400_with_error(id_code)
    payment = db2.session.query(Payment).filter_by(booking_id=id).first()
    if payment:
        if payment.create_datetime is not None:
            payment.create_datetime = str(payment.create_datetime)
        if payment.cancelled_datetime is not None:
            payment.cancelled_datetime = str(payment.cancelled_datetime)
        if payment.refund_datetime is not None:
            payment.refund_datetime = str(payment.refund_datetime)
        json_response = payment_in_json_short(payment)
        json_response = json.dumps(json_response)
        response = Response(json_response, content_type='application/json; charset=utf-8')
        return response
    else:
        return send_400_with_error(2)


@app.route('/refundPayment', methods=['PUT'])
def refund_payment():
    id = request.form.get('id')
    id_code = id_checker(id)
    if id_code != -1:
        return send_400_with_error(id_code)
    payment = db2.session.query(Payment).filter_by(id=id).first()
    if payment is not None:
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if payment.is_refund == 0:
                payment.is_refund = 1
                payment.refund_datetime = date_time
                try:
                    db2.session.commit()
                except ValueError:
                    db2.session.rollback()
                json_response = {"status": "OK",
                                 "id": payment.id,
                                 "refundDatetime": str(payment.refund_datetime)}
                json_response = json.dumps(json_response)
                response = Response(json_response, content_type='application/json; charset=utf-8')
                return response
        else:
            return send_400_with_error(3)
    else:
        return send_400_with_error(2)


@app.route('/cancelBooking', methods=['PUT'])
def cancel_booking():
    id = request.form.get('id')
    cancelled_datetime = request.form.get('cancelledDatetime')
    id_code = id_checker(id)
    if id_code != -1:
        return send_400_with_error(id_code)
    cancelled_datetime_code = check_date_by_format('%Y-%m-%d %H:%M:%S', cancelled_datetime)
    if cancelled_datetime_code != -1:
        return send_400_with_error(cancelled_datetime_code)
    booking = db2.session.query(Booking).filter_by(id=id).first()
    if booking is not None:
        if booking.is_cancelled == 0:
            booking.is_cancelled = 1
            booking.update_datetime = cancelled_datetime
            try:
                db2.session.commit()
            except Exception:
                db2.session.rollback()
            json_response = {'status': 'OK',
                             'id': booking.id}
            json_response = json.dumps(json_response)
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response
        else:
            return send_400_with_error(3)
    else:
        return send_400_with_error(2)


@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='favicon.ico')

db = intour24_database.Database()
db2 = SQLAlchemy(app)
#db.connect(db_name="intour24", host="188.130.155.89", login="intour24_admin", password="R9i477o#W7cv")

import logging
logging.basicConfig()
sqllogger = logging.getLogger('sqlalchemy.engine')
sqllogger.setLevel(logging.DEBUG)
fh = logging.FileHandler('sql.log')
fh.setLevel(logging.DEBUG)
sqllogger.addHandler(fh)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
