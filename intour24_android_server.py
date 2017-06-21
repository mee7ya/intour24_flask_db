import requests
from flask import Flask, url_for, request, json, Response
from nikita_first_python_program import convert
import datetime
import intour24_database
import random
import os


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False
SMS_URL = 'https://sms.ru/sms/'
SMS_API = '1F5F1DF2-3C6B-D268-A754-75F38D147E70'
__directory__ = os.path.dirname(os.path.realpath(__file__));


def send_400_with_error(error):
    json_response = {'status': "ERROR",
                     'error': error}
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response, 400


def id_checker(id):
    if id != '' and id is not None:
        if id.isdigit():
            if int(id) == 0:
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


@app.route('/excursion/<id>')
def excursion(id):
    id_code = id_checker(id)
    if id_code != -1:
        return send_400_with_error(id_code)
    __parameters__ = ['id', 'name', 'description', 'duration', 'priceForChildren', 'priceForAdult',
                      'priceForEnfant', 'pickingPlace', 'category', 'rating', 'properties',
                      'images', 'phone', 'address', 'logo', 'accreditation', 'capacity', 'linkToSite', 'icon']
    sql_file = open(os.path.join(__directory__, 'sql/excursion_by_id.sql'), 'r')
    rows = db.select_custom_query_with_params(sql_file.read(), (id,));
    sql_file.close()
    if rows:
        json_price = {__parameters__[0]: rows[0][12],
                      __parameters__[4]: rows[0][4],
                      __parameters__[5]: rows[0][5],
                      __parameters__[6]: rows[0][6]
                      }
        json_picking_place = {__parameters__[0]: rows[0][13],
                              __parameters__[1]: rows[0][7]}
        json_category = {__parameters__[0]: rows[0][14],
                         __parameters__[1]: rows[0][8],
                         __parameters__[18]: rows[0][25]}
        json_properties = []
        for i in range(len(rows[0][15])):
            json_property = {__parameters__[0]: rows[0][15][i],
                             __parameters__[1]: rows[0][10][i],
                             __parameters__[18]: rows[0][24][i]}
            json_properties.append(json_property)
        json_operator = {__parameters__[0]: rows[0][16],
                         __parameters__[1]: rows[0][17],
                         __parameters__[12]: rows[0][18],
                         __parameters__[13]: rows[0][19],
                         __parameters__[14]: rows[0][20],
                         __parameters__[15]: rows[0][21]}
        json_response = {__parameters__[0]: rows[0][0],
                         __parameters__[1]: rows[0][1],
                         __parameters__[2]: rows[0][2],
                         __parameters__[3]: convert(rows[0][3]),
                         'price': json_price,
                         'pickingPlace': json_picking_place,
                         'category': json_category,
                         __parameters__[9]: rows[0][9],
                         'properties': json_properties,
                         __parameters__[11]: rows[0][11],
                         'operator': json_operator,
                         __parameters__[16]: rows[0][22],
                         __parameters__[17]: rows[0][23]}
        json_response = json.dumps(json_response)
        response = Response(json_response, content_type='application/json; charset=utf-8')
        return response
    else:
        return send_400_with_error(2)


@app.route('/excursions/')
def excursions():
    __parameters__ = ['id', 'name', 'description', 'capacity',
                      'rating', 'duration', 'categoryId', 'startPlaceId', 'operatorId', 'linkToSite', 'images',
                      'priceId']
    __table__ = 'excursions'
    sql_file = open(os.path.join(__directory__, 'sql/excursions.sql'), 'r')
    rows = db.select_custom_query(sql_file.read())
    sql_file.close()
    json_response = []
    for row in rows:
        json_response.append({__parameters__[0]: row[0],
                              __parameters__[1]: row[1],
                              __parameters__[2]: row[2],
                              __parameters__[3]: row[3],
                              __parameters__[4]: row[4],
                              __parameters__[5]: convert(row[5]),
                              __parameters__[6]: row[6],
                              __parameters__[7]: row[7],
                              __parameters__[8]: row[8],
                              __parameters__[9]: row[9],
                              __parameters__[10]: row[10],
                              __parameters__[11]: row[11]
                              })
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/sight/<id>')
def sight(id):
    id_code = id_checker(id)
    if id_code != -1:
        return send_400_with_error(id_code)
    __parameters__ = ['id', 'name', 'geoposition', 'images', 'description', 'cover', 'properties', 'excursions']
    sql_file = open(os.path.join(__directory__, 'sql/sight_by_id.sql'), 'r')
    rows = db.select_custom_query_with_params(sql_file.read(), (id,))
    sql_file.close()
    properties = []
    if rows:
        for i in range(0, len(rows[0][6])):
            properties.append({'name': rows[0][6][i],
                               'icon': rows[0][7][i]})
        json_response = {__parameters__[0]: rows[0][0],
                         __parameters__[1]: rows[0][1],
                         __parameters__[2]: rows[0][2],
                         __parameters__[3]: rows[0][3],
                         __parameters__[4]: rows[0][4],
                         __parameters__[5]: rows[0][5],
                         __parameters__[6]: properties}
        json_response = json.dumps(json_response)
        response = Response(json_response, content_type='application/json; charset=utf-8')
        return response
    else:
        return send_400_with_error(2)


@app.route('/sights/')
def sights():
    __table__ = 'sights'
    __parameters__ = ['id', 'name', 'geoposition', 'images', 'description', 'cover', 'minPrice', 'maxPrice', 'properties']
    __parameters_properties__ = ['id', 'name', 'image']
    query = 'SELECT s.*, array_agg(p.price_for_adult), array_agg(DISTINCT sp.id), array_agg(DISTINCT sp.name), array_agg(DISTINCT sp.image) ' \
            'FROM sights s ' \
            'LEFT JOIN excursions_sights es ' \
            'ON s.id = es.sight_id ' \
            'LEFT JOIN excursions e ' \
            'ON es.excursion_id = e.id ' \
            'LEFT JOIN prices p ' \
            'ON e.price_id = p.id ' \
            'LEFT JOIN sights_sight_property ssp ' \
            'ON s.id = ssp.sight_id ' \
            'LEFT JOIN sight_property sp ' \
            'ON sp.id = ssp.sight_property_id ' \
            'GROUP BY s.id ' \
            'ORDER BY s.id;'
    rows = db.select_custom_query(query=query)
    json_response = []
    for row in rows:
        if row[6][0] is None:
            min_value = None
            max_value = None
        else:
            min_value = min(row[6])
            max_value = max(row[6])
        json_properties = []
        for i in range(len(row[7])):
            json_properties.append({__parameters_properties__[0]: row[7][i],
                                    __parameters_properties__[1]: row[8][i],
                                    __parameters_properties__[2]: row[9][i]})
        json_response.append({__parameters__[0]: row[0],
                              __parameters__[1]: row[1],
                              # __parameters__[2]: row[2],
                              __parameters__[3]: row[3],
                              # __parameters__[4]: row[4],
                              __parameters__[5]: row[5],
                              __parameters__[6]: min_value,
                              __parameters__[7]: max_value,
                              # __parameters__[8]: json_properties
                              })
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/groups/', methods=['POST'])
def groups_upd():
    group_id = request.form.get('group_id')
    seats_reserved = request.form.get('seats_reserved');
    if not (group_id == '' or seats_reserved == '' or group_id is None or seats_reserved is None):
        try:
            if int(group_id) <= 0 or int(seats_reserved) == 0:
                return send_400_with_error(6)
        except ValueError:
            return send_400_with_error(5)
        query = 'SELECT seats_reserved, seats_capacity ' \
                'FROM groups ' \
                'WHERE id= ' + group_id
        rows = db.select_custom_query(query)
        if rows:
            row = rows[0]
            more_seats_reserved = int(row[0])+int(seats_reserved)
            if more_seats_reserved < 0:
                return send_400_with_error(6)
            if more_seats_reserved <= row[1]:
                query = 'UPDATE groups SET seats_reserved = '+str(more_seats_reserved)+' WHERE id = '+group_id+' RETURNING id;'
                db.update_insert_custom_query(query)
                if more_seats_reserved == row[1]:
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
                return send_400_with_error(7)  # need to think
        else:
            return send_400_with_error(2)
    return send_400_with_error(1)


@app.route('/groups/<date>/sight/<sight_id>')
def groups(date, sight_id):
    id_code = id_checker(sight_id)
    if id_code != -1:
        return send_400_with_error(id_code)
    date_code = check_date_by_format('%Y-%m-%d', date)
    if date_code != -1:
        return send_400_with_error(date_code)
    __parameters_group__ = ['id', 'tourDate', 'seatsReserved', 'guideId', 'seatsCapacity', 'excursion']
    __parameters_excursion__ = ['id', 'name', 'description', 'capacity', 'rating', 'duration', 'linkToSite',
                                'images', 'category', 'pickingPlace', 'price', 'properties', 'sight', 'operator']
    __parameters_category__ = ['id', 'name', 'icon']
    __parameters_picking_place__ = ['id', 'name', 'geoposition']
    __parameters_price__ = ['id', 'priceForChildren', 'priceForAdult', 'priceForEnfant']
    __parameters_properties__ = ['id', 'name', 'image']
    __parameters_sight__ = ['id', 'name']
    __parameters_operator__ = ['id', 'name', 'phone', 'address', 'logo', 'accreditation']
    query = "SELECT g.id, g.tour_date, g.seats_reserved, g.guide_id, g.seats_capacity, e.id, e.name, e.description, " \
            "e.capacity, e.average_rating, e.duration, e.link_to_site, e.images, " \
            "c.id, c.name, p.*, pp.*, array_agg(ep.id), array_agg(ep.name), array_agg(ep.icon), s.id, s.name, o.*, c.icon " \
            "FROM groups g " \
            "LEFT JOIN excursions e " \
            "ON g.excursion_id = e.id " \
            "LEFT JOIN category c " \
            "ON e.category_id = c.id " \
            "LEFT JOIN prices p " \
            "ON e.price_id = p.id " \
            "LEFT JOIN picking_places pp " \
            "ON e.picking_place_id = pp.id " \
            "LEFT JOIN excursions_excursion_property eep " \
            "ON eep.excursion_id = e.id " \
            "LEFT JOIN excursion_property ep " \
            "ON ep.id = eep.excursion_property_id " \
            "LEFT JOIN excursions_sights es " \
            "ON es.excursion_id = e.id " \
            "LEFT JOIN sights s " \
            "ON s.id = es.sight_id " \
            "LEFT JOIN operator o " \
            "ON e.operator_id = o.id " \
            "WHERE g.tour_date::date = %s AND s.id = %s " \
            "GROUP BY g.id, e.id, c.id, p.id, pp.id, s.id, o.id " \
            "ORDER BY g.id;"
    rows = db.select_custom_query_with_params(query, (date, sight_id))
    json_response = []
    for row in rows:
        json_category = {__parameters_category__[0]: row[13],
                         __parameters_category__[1]: row[14],
                         __parameters_category__[2]: row[34]}
        json_price = {__parameters_price__[0]: row[15],
                      __parameters_price__[1]: row[16],
                      __parameters_price__[2]: row[17],
                      __parameters_price__[3]: row[18]}
        json_picking_place = {__parameters_picking_place__[0]: row[19],
                              __parameters_picking_place__[1]: row[20],
                              __parameters_picking_place__[2]: row[21]}
        json_properties = []
        for i in range(len(row[22])):
            json_properties.append({__parameters_properties__[0]: row[22][i],
                                    __parameters_properties__[1]: row[23][i],
                                    __parameters_properties__[2]: row[24][i]})
        json_sight = {__parameters_sight__[0]: row[25],
                      __parameters_sight__[1]: row[26]}
        json_operator = {__parameters_operator__[0]: row[27],
                         __parameters_operator__[1]: row[28],
                         __parameters_operator__[2]: row[29],
                         __parameters_operator__[3]: row[30],
                         __parameters_operator__[4]: row[31],
                         __parameters_operator__[5]: row[32]}
        json_excursion = {__parameters_excursion__[0]: row[5],
                          __parameters_excursion__[1]: row[6],
                          __parameters_excursion__[2]: row[7],
                          __parameters_excursion__[3]: row[8],
                          __parameters_excursion__[4]: row[9],
                          __parameters_excursion__[5]: convert(row[10]),
                          __parameters_excursion__[6]: row[11],
                          __parameters_excursion__[7]: row[12],
                          __parameters_excursion__[8]: json_category,
                          __parameters_excursion__[9]: json_picking_place,
                          __parameters_excursion__[10]: json_price,
                          __parameters_excursion__[11]: json_properties,
                          __parameters_excursion__[12]: json_sight,
                          __parameters_excursion__[13]: json_operator}
        json_response.append({__parameters_group__[0]: row[0],
                              __parameters_group__[1]: str(row[1]),
                              __parameters_group__[2]: row[2],
                              __parameters_group__[3]: row[3],
                              __parameters_group__[4]: row[4],
                              __parameters_group__[5]: json_excursion,
                              })
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/group/<id>')
def group(id):
    id_code = id_checker(id)
    if id_code != -1:
        return send_400_with_error(id_code)
    __parameters_group__ = ['id', 'tourDate', 'seatsReserved', 'guideId', 'seatsCapacity', 'excursion']
    __parameters_excursion__ = ['id', 'name', 'description', 'capacity', 'rating', 'duration', 'linkToSite',
                                'images', 'category', 'pickingPlace', 'price', 'properties', 'sight', 'operator']
    __parameters_category__ = ['id', 'name', 'icon']
    __parameters_picking_place__ = ['id', 'name', 'geoposition']
    __parameters_price__ = ['id', 'priceForChildren', 'priceForAdult', 'priceForEnfant']
    __parameters_properties__ = ['id', 'name', 'image']
    __parameters_sight__ = ['id', 'name']
    __parameters_operator__ = ['id', 'name', 'phone', 'address', 'logo', 'accreditation']
    query = 'SELECT g.id, g.tour_date, g.seats_reserved, g.guide_id, g.seats_capacity, e.id, e.name, e.description, ' \
            'e.capacity, e.average_rating, e.duration, e.link_to_site, e.images, ' \
            'c.id, c.name, p.*, pp.*, array_agg(ep.id), array_agg(ep.name), array_agg(ep.icon), s.id, s.name, o.*, c.icon ' \
            'FROM groups g ' \
            'LEFT JOIN excursions e ' \
            'ON g.excursion_id = e.id ' \
            'LEFT JOIN category c ' \
            'ON e.category_id = c.id ' \
            'LEFT JOIN prices p ' \
            'ON e.price_id = p.id ' \
            'LEFT JOIN picking_places pp ' \
            'ON e.picking_place_id = pp.id ' \
            'LEFT JOIN excursions_excursion_property eep ' \
            'ON eep.excursion_id = e.id ' \
            'LEFT JOIN excursion_property ep ' \
            'ON ep.id = eep.excursion_property_id ' \
            'LEFT JOIN excursions_sights es ' \
            'ON es.excursion_id = e.id ' \
            'LEFT JOIN sights s ' \
            'ON s.id = es.sight_id ' \
            'LEFT JOIN operator o ' \
            'ON o.id = e.operator_id ' \
            'WHERE g.id = %s ' \
            'GROUP BY g.id, e.id, c.id, p.id, pp.id, s.id, o.id ' \
            'ORDER BY g.id;'
    rows = db.select_custom_query_with_params(query, (id,))
    if rows:
        for row in rows:
            json_category = {__parameters_category__[0]: row[13],
                             __parameters_category__[1]: row[14],
                             __parameters_category__[2]: row[34]}
            json_price = {__parameters_price__[0]: row[15],
                          __parameters_price__[1]: row[16],
                          __parameters_price__[2]: row[17],
                          __parameters_price__[3]: row[18]}
            json_picking_place = {__parameters_picking_place__[0]: row[19],
                                  __parameters_picking_place__[1]: row[20],
                                  __parameters_picking_place__[2]: row[21]}
            json_properties = []
            for i in range(len(row[22])):
                json_properties.append({__parameters_properties__[0]: row[22][i],
                                        __parameters_properties__[1]: row[23][i],
                                        __parameters_properties__[2]: row[24][i]})
            json_sight = {__parameters_sight__[0]: row[25],
                          __parameters_sight__[1]: row[26]}
            json_operator = {__parameters_operator__[0]: row[27],
                             __parameters_operator__[1]: row[28],
                             __parameters_operator__[2]: row[29],
                             __parameters_operator__[3]: row[30],
                             __parameters_operator__[4]: row[31],
                             __parameters_operator__[5]: row[32]}
            json_excursion = {__parameters_excursion__[0]: row[5],
                              __parameters_excursion__[1]: row[6],
                              __parameters_excursion__[2]: row[7],
                              __parameters_excursion__[3]: row[8],
                              __parameters_excursion__[4]: row[9],
                              __parameters_excursion__[5]: convert(row[10]),
                              __parameters_excursion__[6]: row[11],
                              __parameters_excursion__[7]: row[12],
                              __parameters_excursion__[8]: json_category,
                              __parameters_excursion__[9]: json_picking_place,
                              __parameters_excursion__[10]: json_price,
                              __parameters_excursion__[11]: json_properties,
                              __parameters_excursion__[12]: json_sight,
                              __parameters_excursion__[13]: json_operator}
            json_response = {__parameters_group__[0]: row[0],
                                  __parameters_group__[1]: str(row[1]),
                                  __parameters_group__[2]: row[2],
                                  __parameters_group__[3]: row[3],
                                  __parameters_group__[4]: row[4],
                                  __parameters_group__[5]: json_excursion,
                                  }
        json_response = json.dumps(json_response)
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
    query = "SELECT seats_reserved, seats_capacity FROM groups WHERE id=%s"
    rows = db.select_custom_query_with_params(query, (group_id,))
    if rows:
        people_reserved = int(rows[0][0]) + int(children) + int(adults) + int(enfants)
        people_capacity = int(rows[0][1])
        if int(people_reserved) <= int(people_capacity):
            query = "INSERT INTO bookings(tourist_id, group_id, adults, children, " \
                    "enfants, total_price, create_datetime, is_cancelled) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, 0) " \
                    "RETURNING id, create_datetime; "
            c_id = db.update_insert_custom_query_if_not_exists_with_params(query, (tourist_id, group_id, adults, children,
                                                                     enfants, total_price, create_datetime))
            if people_capacity == people_reserved:
                json_response = {'status': 'OK',
                                 'full': 1,
                                 'id': c_id[0],
                                 'created': str(c_id[1])}
                json_response = json.dumps(json_response)
                response = Response(json_response, content_type='application/json; charset=utf-8')
                return response
            else:
                json_response = {'status': 'OK',
                                'full': 0,
                                'id': c_id[0],
                                'created': str(c_id[1])}
                json_response = json.dumps(json_response)
                response = Response(json_response, content_type='application/json; charset=utf-8')
                return response
        else:
            return send_400_with_error(7)
    else:
        return send_400_with_error(2)


@app.route('/bookingsByTouristId/<tourist_id>')
def bookings(tourist_id):
    tourist_id_code = id_checker(tourist_id)
    if tourist_id_code != -1:
        return send_400_with_error(tourist_id_code)
    __parameters_booking__ = ['id', 'excursion', 'totalPrice', 'paymentId', 'group', 'isCancelled']
    __parameters_excursion__ = ['id', 'name', 'pickingPlace', 'duration', 'operator']
    __parameters_picking_place__ = ['id', 'name']
    __parameters_group__ = ['id', 'tourDate']
    __parameters_operator__ = ['id', 'name', 'phone', 'address', 'logo', 'accreditation', 'email']
    query = "SELECT b.id, b.total_price, p.id, e.id, e.name, e.duration, pp.id, pp.name, g.id, g.tour_date, " \
            "b.is_cancelled, o.id, o.name, o.phone, o.address, o.logo, o.accreditation, o.email, b.create_datetime " \
            "FROM bookings b " \
            "LEFT JOIN payments p " \
            "ON b.id = p.booking_id " \
            "LEFT JOIN groups g " \
            "ON b.group_id = g.id " \
            "LEFT JOIN excursions e " \
            "ON g.excursion_id = e.id " \
            "LEFT JOIN picking_places pp " \
            "ON e.picking_place_id = pp.id " \
            "LEFT JOIN operator o " \
            "ON o.id = e.operator_id " \
            "WHERE b.tourist_id = %s " \
            "GROUP BY b.id, p.id, pp.id, g.id, e.id, o.id " \
            "ORDER BY b.id "
    rows = db.select_custom_query_with_params(query, (tourist_id,))
    if rows:
        json_response = []
        for row in rows:
            json_picking_place = {__parameters_picking_place__[0]: row[6],
                                  __parameters_picking_place__[1]: row[7]}
            json_group = {__parameters_group__[0]: row[8],
                          __parameters_group__[1]: str(row[9])}
            json_operator = {__parameters_operator__[0]: row[11],
                             __parameters_operator__[1]: row[12],
                             __parameters_operator__[2]: row[13],
                             __parameters_operator__[3]: row[14],
                             __parameters_operator__[4]: row[15],
                             __parameters_operator__[5]: row[16],
                             __parameters_operator__[6]: row[17]}
            json_excursion = {__parameters_excursion__[0]: row[3],
                              __parameters_excursion__[1]: row[4],
                              __parameters_excursion__[2]: json_picking_place,
                              __parameters_excursion__[3]: convert(row[5]),
                              __parameters_excursion__[4]: json_operator}
            json_response.append({__parameters_booking__[0]: row[0],
                                  __parameters_booking__[1]: json_excursion,
                                  __parameters_booking__[2]: row[1],
                                  __parameters_booking__[3]: row[2],
                                  __parameters_booking__[4]: json_group,
                                  __parameters_booking__[5]: row[10],
                                  'created': str(row[18])})
        json_response = json.dumps(json_response)
        response = Response(json_response, content_type='application/json; charset=utf-8')
        return response
    else:
        return send_400_with_error(2)


@app.route('/booking/<id>')
def booking(id):
        id_code = id_checker(id)
        if id_code != -1:
            return send_400_with_error(id_code)
        __parameters__ = ['id', 'adults', 'children', 'enfants', 'totalPrice', 'group']
        __parameters_group__ = ['id', 'tourDate', 'excursion']
        __parameters_excursion__ = ['id', 'name', 'duration', 'operator', 'pickingPlace', 'properties']
        __parameters_picking_place__ = ['id', 'name', 'geoposition']
        __parameters_properties__ = ['id', 'name', 'icon']
        __parameters_operator__ = ['id', 'name', 'logo']
        query = 'SELECT b.id, b.adults, b.children, b.enfants, b.total_price, g.id, g.tour_date, e.id, e.name, ' \
                'e.duration, o.id, o.name, o.logo, pp.id, pp.name, pp.geoposition, ' \
                'array_agg(ep.id), array_agg(ep.name), array_agg(ep.icon) ' \
                'FROM bookings b ' \
                'LEFT JOIN groups g ' \
                'ON g.id = b.group_id ' \
                'LEFT JOIN excursions e ' \
                'ON g.excursion_id = e.id ' \
                'LEFT JOIN operator o ' \
                'ON e.operator_id = o.id ' \
                'LEFT JOIN picking_places pp ' \
                'ON e.picking_place_id = pp.id ' \
                'LEFT JOIN excursions_excursion_property eep ' \
                'ON eep.excursion_id = e.id ' \
                'LEFT JOIN excursion_property ep ' \
                'ON eep.excursion_property_id = ep.id ' \
                'WHERE b.id = %s ' \
                'GROUP BY b.id, g.id, e.id, o.id, pp.id ' \
                'ORDER BY b.id '
        rows = db.select_custom_query_with_params(query, (id,))
        if rows:
            row = rows[0]
            json_properties = []
            for i in range(len(row[16])):
                json_properties.append({__parameters_properties__[0]: row[16][i],
                                        __parameters_properties__[1]: row[17][i],
                                        __parameters_properties__[2]: row[18][i]})
            json_operator = {__parameters_operator__[0]: row[10],
                             __parameters_operator__[1]: row[11],
                             __parameters_operator__[2]: row[12]}
            json_picking_place = {__parameters_picking_place__[0]: row[13],
                                  __parameters_picking_place__[1]: row[14],
                                  __parameters_picking_place__[2]: row[15]}
            json_excursion = {__parameters_excursion__[0]: row[7],
                              __parameters_excursion__[1]: row[8],
                              __parameters_excursion__[2]: convert(row[9]),
                              __parameters_excursion__[3]: json_operator,
                              __parameters_excursion__[4]: json_picking_place,
                              __parameters_excursion__[5]: json_properties}
            json_group = {__parameters_group__[0]: row[5],
                          __parameters_group__[1]: str(row[6]),
                          __parameters_group__[2]: json_excursion}
            json_response = {__parameters__[0]: row[0],
                             __parameters__[1]: row[1],
                             __parameters__[2]: row[2],
                             __parameters__[3]: row[3],
                             __parameters__[4]: row[4],
                             __parameters__[5]: json_group}
            json_response = json.dumps(json_response)
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
    query = "SELECT id FROM bookings WHERE id = %s"
    rows = db.select_custom_query_with_params(query, (booking_id,))
    if rows:
        query = "INSERT INTO payments (booking_id, create_datetime, identifier, is_cancelled, is_refund) " \
                "SELECT %s, %s, %s, 0, 0 " \
                "WHERE NOT EXISTS (SELECT booking_id FROM payments WHERE booking_id = %s) " \
                "RETURNING id;"
        c_id = db.update_insert_custom_query_if_not_exists_with_params(query, (booking_id, payment_time,
                                                                               identifier, booking_id))
        if c_id:
            json_response = {'status': "OK",
                             'paymentId': c_id[0],
                             'createDatetime': payment_time}
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
    query = "SELECT id FROM tourists WHERE phone = %s"
    rows = db.select_custom_query_with_params(query, (phone,))
    if rows:
        code = generate_code()
        if send_sms(code, phone):
            json_response = {"status": "OK",
                             "registered": 1,
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
        if len(name) > 60:
            return send_400_with_error(6)
        if phone.isdigit():
            query = "INSERT INTO tourists (first_name, phone) " \
                    "SELECT '"+name+"', '"+phone+"' " \
                    "WHERE NOT EXISTS (SELECT id FROM tourists WHERE phone = '"+phone+"')" \
                    "RETURNING id;"
            c_id = db.update_insert_custom_query_if_not_exists(query)
            if c_id is not None:
                code = generate_code()
                send_sms(code, phone)
                json_response = {"status": "OK",
                                 "id": +c_id[0],
                                 "code": code}
            else:
                json_response = {"status": "ERROR",
                                 "id": 0,
                                 "code": 0}
            json_response = json.dumps(json_response)
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response
        else:
            try:
                if int(phone) < 0:
                    return send_400_with_error(6)
            except ValueError:
                return send_400_with_error(5)
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
        if len(name) > 60:
            return send_400_with_error(6)
        return send_400_with_error(1)
    query = "UPDATE tourists SET first_name = %s, phone = %s WHERE id = %s RETURNING id;"
    c_id = db.update_insert_custom_query_if_not_exists_with_params(query, (name, phone, c_id))
    if c_id is not None:
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
    query = "SELECT id FROM payments WHERE booking_id = %s AND is_cancelled = 1"
    rows = db.select_custom_query_with_params(query, (booking_id,))
    if not rows:
        query = "UPDATE payments SET is_cancelled = 1, cancelled_datetime = %s WHERE booking_id = %s RETURNING id"
        payment_id = db.update_insert_custom_query_if_not_exists_with_params(query, (cancelled_datetime, booking_id))
        if payment_id is not None:
            query = "UPDATE bookings SET is_cancelled = 1, update_datetime = %s WHERE id = %s RETURNING id"
            booking_id = db.update_insert_custom_query_if_not_exists_with_params(query, (cancelled_datetime, booking_id))
            json_response = {"status": "OK",
                             "paymentId": payment_id[0],
                             "bookingId": booking_id[0]}
            json_response = json.dumps(json_response)
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response
        send_400_with_error(2)
    else:
        send_400_with_error(3)


@app.route('/paymentByBookingId/<id>')
def payment_by_booking_id(id):
    id_code = id_checker(id)
    if id_code != -1:
        return send_400_with_error(id_code)
    __parameters_payment__ = ['id', 'bookingId', 'createDatetime', 'cancelledDatetime',
                              'refundDatetime', 'isCancelled', 'isRefund', 'identifier']
    query = "SELECT * FROM payments WHERE booking_id= %s"
    rows = db.select_custom_query_with_params(query, (id,))
    if rows:
        row = rows[0]
        formatted_create_datetime = None
        formatted_cancel_datetime = None
        formatted_refund_datetime = None
        if row[2] is not None:
            formatted_create_datetime = str(row[2])
        if row[3] is not None:
            formatted_cancel_datetime = str(row[3])
        if row[4] is not None:
            formatted_refund_datetime = str(row[4])
        json_response = {__parameters_payment__[0]: row[0],
                         __parameters_payment__[1]: row[1],
                         __parameters_payment__[2]: formatted_create_datetime,
                         __parameters_payment__[3]: formatted_cancel_datetime,
                         __parameters_payment__[4]: formatted_refund_datetime,
                         __parameters_payment__[5]: row[5],
                         __parameters_payment__[6]: row[6],
                         __parameters_payment__[7]: row[7]}
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
    query = "SELECT id FROM payments WHERE id = %s AND is_refund = 1"
    db_response = db.select_custom_query_with_params(query, (id,))
    if db_response:
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "UPDATE payments SET is_refund = 1, refund_datetime = %s WHERE id = %s RETURNING id, refund_datetime;"
        db_response = db.update_insert_custom_query_if_not_exists_with_params(query, (date_time, id))
        if db_response:
            json_response = {"status": "OK",
                             "id": db_response[0],
                             "refundDatetime": str(db_response[1])}
            json_response = json.dumps(json_response)
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response
        else:
            return send_400_with_error(2)
    else:
        return send_400_with_error(3)


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
    query = "UPDATE bookings SET is_cancelled = 1, update_datetime = %s WHERE id = %s RETURNING id"
    c_id = db.update_insert_custom_query_if_not_exists_with_params(query, (cancelled_datetime, id))
    if c_id:
        json_response = {'status': 'OK',
                         'id': c_id[0]}
        json_response = json.dumps(json_response)
        response = Response(json_response, content_type='application/json; charset=utf-8')
        return response
    else:
        return send_400_with_error(2)


@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='favicon.ico')


db = intour24_database.Database()
db.connect(db_name="intour24", host="188.130.155.89", login="intour24_admin", password="R9i477o#W7cv")
if __name__ == '__main__':
    app.run(host='0.0.0.0');
