from flask import Flask, url_for, request, json, Response
from nikita_first_python_program import convert
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import intour24_database


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False
schedule = BlockingScheduler()


@app.route('/excursion/<id>')
def excursion(id):
    if id.isdigit():
        __table__ = 'excursions'
        __parameters__ = ['id', 'name', 'description', 'duration', 'priceForChildren', 'priceForAdult',
                          'priceForEnfant', 'pickingPlace', 'category', 'rating', 'properties',
                          'images']
        query = 'SELECT e.id, e.name, e.description, e.duration, p.price_for_children, p.price_for_adult, ' \
                'p.price_for_enfant, pp.name, c.name, ' \
                'e.average_rating, array_agg(ep.name), e.images ' \
                'FROM excursions e ' \
                'LEFT JOIN prices p ' \
                'ON e.price_id = p.id ' \
                'LEFT JOIN picking_places pp ' \
                'ON e.picking_place_id = pp.id ' \
                'LEFT JOIN category c ' \
                'ON e.category_id = c.id ' \
                'LEFT JOIN excursions_excursion_property eep ' \
                'ON e.id = eep.excursion_id ' \
                'LEFT JOIN excursion_property ep ' \
                'ON ep.id = eep.excursion_property_id ' \
                'WHERE e.id =  ' + id + \
                'GROUP BY e.id, p.price_for_children, p.price_for_adult, p.price_for_enfant, ' \
                'pp.name, e.average_rating, c.name'
        rows = db.select_custom_query(query=query);
        if rows:
            json_response = {__parameters__[0]: rows[0][0],
                             __parameters__[1]: rows[0][1],
                             __parameters__[2]: rows[0][2],
                             __parameters__[3]: convert(rows[0][3]),
                             __parameters__[4]: rows[0][4],
                             __parameters__[5]: rows[0][5],
                             __parameters__[6]: rows[0][6],
                             __parameters__[7]: rows[0][7],
                             __parameters__[8]: rows[0][8],
                             __parameters__[9]: rows[0][9],
                             __parameters__[10]: rows[0][10],
                             __parameters__[11]: rows[0][11]}
            json_response = json.dumps(json_response)
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response
        else:
            json_response = {'error': 'wrong input'}
            json_response = json.dumps(json_response)
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response, 400
    else:
        json_response = {'error': 'wrong input'}
        json_response = json.dumps(json_response)
        response = Response(json_response, content_type='application/json; charset=utf-8')
        return response, 400


@app.route('/excursions/')
def excursions():
    __parameters__ = ['id', 'name', 'description', 'capacity',
                      'averageRating', 'duration', 'categoryId', 'startPlaceId', 'operatorId', 'link_to_site', 'images',
                      'priceId']
    __table__ = 'excursions'
    rows = db.select_query(table=__table__)
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
    if id.isdigit():
        __table__ = 'sights'
        __parameters__ = ['id', 'name', 'geoposition', 'images', 'description', 'cover', 'properties', 'excursions']
        query = 'SELECT s.*, array_agg(DISTINCT sp.name), array_agg(DISTINCT sp.image), array_agg(DISTINCT e.name) ' \
                'FROM sights s ' \
                'LEFT JOIN sights_sight_property ssp ' \
                'ON s.id = ssp.sight_id ' \
                'LEFT JOIN sight_property sp ' \
                'ON ssp.sight_property_id = sp.id ' \
                'LEFT JOIN excursions_sights es ' \
                'ON es.sight_id = s.id ' \
                'LEFT JOIN excursions e ' \
                'ON e.id = es.excursion_id ' \
                'WHERE s.id = ' + id + \
                'GROUP BY s.id ' \
                'ORDER BY s.id;'
        rows = db.select_custom_query(query=query)
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
                             __parameters__[6]: properties,
                             __parameters__[7]: rows[0][8]}
            json_response = json.dumps(json_response)
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response
        else:
            json_response = {'error': 'wrong input'}
            json_response = json.dumps(json_response)
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response, 400
    else:
        json_response = {'error': 'wrong input'}
        json_response = json.dumps(json_response)
        response = Response(json_response, content_type='application/json; charset=utf-8')
        return response, 400


@app.route('/sights/')
def sights():
    __table__ = 'sights'
    __parameters__ = ['id', 'name', 'geoposition', 'images', 'description', 'cover', 'minPrice', 'maxPrice']
    query = 'SELECT s.*, array_agg(p.price_for_adult) ' \
            'FROM sights s ' \
            'LEFT JOIN excursions_sights es ' \
            'ON s.id = es.sight_id ' \
            'LEFT JOIN excursions e ' \
            'ON es.excursion_id = e.id ' \
            'LEFT JOIN prices p ' \
            'ON e.price_id = p.id ' \
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
        json_response.append({__parameters__[0]: row[0],
                              __parameters__[1]: row[1],
                              __parameters__[2]: row[2],
                              __parameters__[3]: row[3],
                              __parameters__[4]: row[4],
                              __parameters__[5]: row[5],
                              __parameters__[6]: min_value,
                              __parameters__[7]: max_value})
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/category')
def category():
    __table__ = 'category'
    __parameters__ = ['id', 'name']
    c_id = request.args.get('id')
    if c_id is None:
        rows = db.select_query(table=__table__)
        json_response = []
        for row in rows:
            json_response.append({__parameters__[0]: row[0],
                                  __parameters__[1]: row[1]})
        json_response = json.dumps(json_response)
    else:
        rows = db.select_query_with_id(table=__table__, c_id=c_id)
        json_response = {__parameters__[0]: rows[0][0],
                         __parameters__[1]: rows[0][1]}
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/picking_places')
def picking_places():
    __table__ = 'picking_places'
    __parameters__ = ['id', 'name', 'geoposition']
    c_id = request.args.get('id')
    if c_id is None:
        rows = db.select_query(table=__table__)
        json_response = []
        for row in rows:
            json_response.append({__parameters__[0]: row[0],
                                  __parameters__[1]: row[1],
                                  __parameters__[2]: row[2]})
    else:
        rows = db.select_query_with_id(table=__table__, c_id=c_id)
        json_response = {__parameters__[0]: rows[0][0],
                         __parameters__[1]: rows[0][1],
                         __parameters__[2]: rows[0][2]}
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/operator')
def operator():
    __table__ = 'operator'
    __parameters__ = ['id', 'name', 'phone', 'address', 'logo']
    c_id = request.args.get('id')
    if c_id is None:
        rows = db.select_query(table=__table__)
        json_response = []
        for row in rows:
            json_response.append({__parameters__[0]: row[0],
                                  __parameters__[1]: row[1],
                                  __parameters__[2]: row[2]})
    else:
        rows = db.select_query_with_id(table=__table__, c_id=c_id)
        json_response = {__parameters__[0]: rows[0][0],
                         __parameters__[1]: rows[0][1],
                         __parameters__[2]: rows[0][2]}
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/guides')
def guides():
    __table__ = 'guides'
    __parameters__ = ['id', 'first_name', 'e-mail', 'phone', 'last_name', 'average_rating']
    c_id = request.args.get('id')
    if c_id is None:
        rows = db.select_query(table=__table__)
        json_response = []
        for row in rows:
            json_response.append({__parameters__[0]: row[0],
                                  __parameters__[1]: row[1],
                                  __parameters__[2]: row[2],
                                  __parameters__[3]: row[3],
                                  __parameters__[4]: row[4],
                                  __parameters__[5]: row[5]})
    else:
        rows = db.select_query_with_id(table=__table__, c_id=c_id)
        json_response = {__parameters__[0]: rows[0][0],
                         __parameters__[1]: rows[0][1],
                         __parameters__[2]: rows[0][2],
                         __parameters__[3]: rows[0][3],
                         __parameters__[4]: rows[0][4],
                         __parameters__[5]: rows[0][5]}
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/schedule')
def schedule():
    __table__ = 'schedule'
    __parameters__ = ['id', 'tour_date', 'repeat_interval', 'repeat_weekday', 'repeat_week',
                      'end_date', 'excursion_id', 'repeat_year', 'repeat_month', 'repeat_day']
    c_id = request.args.get('id')
    if c_id is None:
        rows = db.select_query(table=__table__)
        json_response = []
        for row in rows:
            json_response.append({__parameters__[0]: row[0],
                                  __parameters__[1]: row[1],
                                  __parameters__[2]: row[2],
                                  __parameters__[3]: row[3],
                                  __parameters__[4]: row[4],
                                  __parameters__[5]: row[5],
                                  __parameters__[6]: row[6],
                                  __parameters__[7]: row[7],
                                  __parameters__[8]: row[8],
                                  __parameters__[9]: row[9]})
    else:
        rows = db.select_query_with_id(table=__table__, c_id=c_id)
        json_response = {__parameters__[0]: rows[0][0],
                         __parameters__[1]: rows[0][1],
                         __parameters__[2]: rows[0][2],
                         __parameters__[3]: rows[0][3],
                         __parameters__[4]: rows[0][4],
                         __parameters__[5]: rows[0][5],
                         __parameters__[6]: rows[0][6],
                         __parameters__[7]: rows[0][7],
                         __parameters__[8]: rows[0][8],
                         __parameters__[9]: rows[0][9]}

    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/groups/', methods=['POST'])
def groups_upd():
    request.accept_mimetypes.best_match(['application/x-www-form-urlencoded'])
    group_id = request.form['group_id']
    seats_reserved = request.form['seats_reserved']
    if not (group_id is None or seats_reserved is None):
        __table__ = 'groups'
        query = 'SELECT seats_reserved, seats_capacity ' \
                'FROM groups ' \
                'WHERE id= ' + group_id
        rows = db.select_custom_query(query)
        row = rows[0]
        more_seats_reserved = int(row[0])+int(seats_reserved)
        if more_seats_reserved <= row[1]:
            query = 'UPDATE groups SET seats_reserved = '+str(more_seats_reserved)+' WHERE id = '+group_id
            db.update_custom_query(query)
            json_response = {'group_id': int(group_id),
                             'seats_reserved': more_seats_reserved}
            json_response = json.dumps(json_response)
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response
        else:
            json_response = {'error': 1}
            json_response = json.dumps(json_response)
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response
    else:
        json_response = {'error': 3}
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response, 400


@app.route('/groups/<date>/sight/<sight_id>')
def groups(date, sight_id):
    __table__ = 'groups'
    __parameters_group__ = ['id', 'tour_date', 'seats_reserved', 'guide_id', 'seats_capacity', 'excursion']
    __parameters_excursion__ = ['id', 'name', 'description', 'capacity', 'average_rating', 'duration', 'linkToSite',
                                'images', 'category', 'picking_place', 'price', 'properties', 'sight']
    __parameters_category__ = ['id', 'name']
    __parameters_picking_place__ = ['id', 'name', 'geoposition']
    __parameters_price__ = ['id', 'price_for_children', 'price_for_adult', 'price_for_enfant']
    __parameters_properties__ = ['id', 'name', 'image']
    __parameters_sight__ = ['id', 'name']
    incorrect_input = True
    if date is not None and sight_id is not None:
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            if sight_id.isdigit():
                incorrect_input = False
            else:
                raise ValueError('id is not digit')
        except ValueError:
            incorrect_input = True
        where_clause = "WHERE g.tour_date::date = '"+date+"' AND s.id = "+sight_id
    else:
        where_clause = ''
    if not incorrect_input:
        query = 'SELECT g.id, g.tour_date, g.seats_reserved, g.guide_id, g.seats_capacity, e.id, e.name, e.description, ' \
                'e.capacity, e.average_rating, e.duration, e.link_to_site, e.images, ' \
                'c.*, p.*, pp.*, array_agg(ep.id), array_agg(ep.name), array_agg(ep.image), s.id, s.name ' \
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
                '' + where_clause + \
                'GROUP BY g.id, e.id, c.id, p.id, pp.id, s.id ' \
                'ORDER BY g.id;'
        rows = db.select_custom_query(query=query)
        json_response = []
        if rows:
            for row in rows:
                json_category = {__parameters_category__[0]: row[13],
                                 __parameters_category__[1]: row[14]}
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
                                  __parameters_excursion__[12]: json_sight}
                json_response.append({__parameters_group__[0]: row[0],
                                      __parameters_group__[1]: row[1],
                                      __parameters_group__[2]: row[2],
                                      __parameters_group__[3]: row[3],
                                      __parameters_group__[4]: row[4],
                                      __parameters_group__[5]: json_excursion,
                                      })
            json_response = json.dumps(json_response)
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response
        else:
            json_response = {'error': 'wrong input'}
            json_response = json.dumps(json_response)
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response, 400
    else:
        json_response = {'error': 'wrong input'}
        json_response = json.dumps(json_response)
        response = Response(json_response, content_type='application/json; charset=utf-8')
        return response, 400


# @app.route('/groups/')
# def groupsAll():
#     __table__ = 'groups'
#     __parameters__ = ['id', 'tour_date', 'seats_reserved', 'excursions_id', 'guide_id',
#                       'seats_capacity']
#     rows = db.select_query(table=__table__)
#     json_response = []
#     for row in rows:
#         json_response.append({__parameters__[0]: row[0],
#                          __parameters__[1]: row[1],
#                          __parameters__[2]: row[2],
#                          __parameters__[3]: row[3],
#                          __parameters__[4]: row[4],
#                          __parameters__[5]: row[5]})
#     json_response = json.dumps(json_response)
#     response = Response(json_response, content_type='application/json; charset=utf-8')
#     return response
#
#
# @app.route('/prices')
# def prices():
#     __table__ = 'prices'
#     __parameters__ = ['id', 'price_for_children', 'price_for_adult', 'price_for_enfant']
#     c_id = request.args.get('id')
#     if c_id is None:
#         rows = db.select_query(table=__table__)
#         json_response = []
#         for row in rows:
#             json_response.append({__parameters__[0]: row[0],
#                                   __parameters__[1]: row[1],
#                                   __parameters__[2]: row[2],
#                                   __parameters__[3]: row[3]
#                                   })
#     else:
#         rows = db.select_query_with_id(table=__table__, c_id=c_id)
#         json_response = {__parameters__[0]: rows[0][0],
#                          __parameters__[1]: rows[0][1],
#                          __parameters__[2]: rows[0][2],
#                          __parameters__[3]: rows[0][3]}
#     json_response = json.dumps(json_response)
#     response = Response(json_response, content_type='application/json; charset=utf-8')
#     return response


@app.route('/excursion_property')
def excursion_property():
    __table__ = 'excursion_property'
    __parameters__ = ['id', 'name', 'image']
    c_id = request.args.get('id')
    if c_id is None:
        rows = db.select_query(table=__table__)
        json_response = []
        for row in rows:
            json_response.append({__parameters__[0]: row[0],
                                  __parameters__[1]: row[1],
                                  __parameters__[2]: row[2]})
    else:
        rows = db.select_query_with_id(table=__table__, c_id=c_id)
        json_response = {__parameters__[0]: rows[0][0],
                         __parameters__[1]: rows[0][1],
                         __parameters__[2]: rows[0][2]}
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/excursions_excursion_property')
def excursions_excursion_property():
    __table__ = 'excursions_excursion_property'
    __parameters__ = ['id', 'excursion_id', 'excursion_property_id']
    c_id = request.args.get('id')
    if c_id is None:
        rows = db.select_query(table=__table__)
        json_response = []
        for row in rows:
            json_response.append({__parameters__[0]: row[0],
                                  __parameters__[1]: row[1],
                                  __parameters__[2]: row[2]
                                  })
    else:
        rows = db.select_query_with_id(table=__table__, c_id=c_id)
        json_response = {__parameters__[0]: rows[0][0],
                         __parameters__[1]: rows[0][1],
                         __parameters__[2]: rows[0][2]}
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/transport_type')
def transport_type():
    __table__ = 'transport_type'
    __parameters__ = ['id', 'name', 'transport_id']
    c_id = request.args.get('id')
    if c_id is None:
        rows = db.select_query(table=__table__)
        json_response = []
        for row in rows:
            json_response.append({__parameters__[0]: row[0],
                                  __parameters__[1]: row[1],
                                  __parameters__[2]: row[2]
                                  })
    else:
        rows = db.select_query_with_id(table=__table__, c_id=c_id)
        json_response = {__parameters__[0]: rows[0][0],
                         __parameters__[1]: rows[0][1],
                         __parameters__[2]: rows[0][2]}
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/transport')
def transport():
    __table__ = 'transport'
    __parameters__ = ['id', 'capacity', 'number', 'group_id']
    c_id = request.args.get('id')
    if c_id is None:
        rows = db.select_query(table=__table__)
        json_response = []
        for row in rows:
            json_response.append({__parameters__[0]: row[0],
                                  __parameters__[1]: row[1],
                                  __parameters__[2]: row[2],
                                  __parameters__[3]: row[3]
                                  })
    else:
        rows = db.select_query_with_id(table=__table__, c_id=c_id)
        json_response = {__parameters__[0]: rows[0][0],
                         __parameters__[1]: rows[0][1],
                         __parameters__[2]: rows[0][2],
                         __parameters__[2]: rows[0][2]}
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/reviews')
def reviews():
    __table__ = 'reviews'
    __parameters__ = ['id', 'excursion_id', 'guide_id', 'excursion_rate', 'guide_rate', 'feedback']
    c_id = request.args.get('id')
    if c_id is None:
        rows = db.select_query(table=__table__)
        json_response = []
        for row in rows:
            json_response.append({__parameters__[0]: row[0],
                                  __parameters__[1]: row[1],
                                  __parameters__[2]: row[2],
                                  __parameters__[3]: row[3],
                                  __parameters__[4]: row[4],
                                  __parameters__[5]: row[5]
                                  })
    else:
        rows = db.select_query_with_id(table=__table__, c_id=c_id)
        json_response = {__parameters__[0]: rows[0][0],
                         __parameters__[1]: rows[0][1],
                         __parameters__[2]: rows[0][2],
                         __parameters__[3]: rows[0][3],
                         __parameters__[4]: rows[0][4],
                         __parameters__[5]: rows[0][5]}
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/bookings')
def bookings():
    __table__ = 'bookings'
    __parameters__ = ['id', 'tourist_id', 'group_id', 'adults', 'children', 'enfants',
                      'payment_date', 'amount', 'payment_identifier']
    c_id = request.args.get('id')
    if c_id is None:
        rows = db.select_query(table=__table__)
        json_response = []
        for row in rows:
            json_response.append({__parameters__[0]: row[0],
                                  __parameters__[1]: row[1],
                                  __parameters__[2]: row[2],
                                  __parameters__[3]: row[3],
                                  __parameters__[4]: row[4],
                                  __parameters__[5]: row[5],
                                  __parameters__[6]: row[6],
                                  __parameters__[7]: row[7],
                                  __parameters__[8]: row[8],
                                  })
    else:
        rows = db.select_query_with_id(table=__table__, c_id=c_id)
        json_response = {__parameters__[0]: rows[0][0],
                         __parameters__[1]: rows[0][1],
                         __parameters__[2]: rows[0][2],
                         __parameters__[3]: rows[0][3],
                         __parameters__[4]: rows[0][4],
                         __parameters__[5]: rows[0][5],
                         __parameters__[6]: rows[0][6],
                         __parameters__[7]: rows[0][7],
                         __parameters__[8]: rows[0][8]}
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/tourists')
def tourists():
    __table__ = 'tourists'
    __parameters__ = ['id', 'first_name', 'email', 'phone', 'last_name']
    c_id = request.args.get('id')
    if c_id is None:
        rows = db.select_query(table=__table__)
        json_response = []
        for row in rows:
            json_response.append({__parameters__[0]: row[0],
                                  __parameters__[1]: row[1],
                                  __parameters__[2]: row[2],
                                  __parameters__[3]: row[3],
                                  __parameters__[4]: row[4]
                                  })
    else:
        rows = db.select_query_with_id(table=__table__, c_id=c_id)
        json_response = {__parameters__[0]: rows[0][0],
                         __parameters__[1]: rows[0][1],
                         __parameters__[2]: rows[0][2],
                         __parameters__[3]: rows[0][3],
                         __parameters__[4]: rows[0][4]}
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/sight_property')
def sight_property():
    __table__ = 'sight_property'
    __parameters__ = ['id', 'name', 'image']
    c_id = request.args.get('id')
    if c_id is None:
        rows = db.select_query(table=__table__)
        json_response = []
        for row in rows:
            json_response.append({__parameters__[0]: row[0],
                                  __parameters__[1]: row[1],
                                  __parameters__[2]: row[2],
                                  })
    else:
        rows = db.select_query_with_id(table=__table__, c_id=c_id)
        json_response = {__parameters__[0]: rows[0][0],
                         __parameters__[1]: rows[0][1],
                         __parameters__[2]: rows[0][2]}
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/excursions_sights')
def excursions_sights():
    __table__ = 'excursions_sights'
    __parameters__ = ['id', 'excursion_id', 'sight_id']
    c_id = request.args.get('id')
    if c_id is None:
        rows = db.select_query(table=__table__)
        json_response = []
        for row in rows:
            json_response.append({__parameters__[0]: row[0],
                                  __parameters__[1]: row[1],
                                  __parameters__[2]: row[2],
                                  })
    else:
        rows = db.select_query_with_id(table=__table__, c_id=c_id)
        json_response = {__parameters__[0]: rows[0][0],
                         __parameters__[1]: rows[0][1],
                         __parameters__[2]: rows[0][2]}
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/sights_sight_property')
def sights_sight_property():
    __table__ = 'sights_sight_property'
    __parameters__ = ['id', 'sight_id', 'sight_property_id']
    c_id = request.args.get('id')
    if c_id is None:
        rows = db.select_query(table=__table__)
        json_response = []
        for row in rows:
            json_response.append({__parameters__[0]: row[0],
                                  __parameters__[1]: row[1],
                                  __parameters__[2]: row[2],
                                  })
    else:
        rows = db.select_query_with_id(table=__table__, c_id=c_id)
        json_response = {__parameters__[0]: rows[0][0],
                         __parameters__[1]: rows[0][1],
                         __parameters__[2]: rows[0][2]}
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='favicon.ico')


@app.route('/')
def ap2():
    return 'api'

# @schedule.scheduled_job('cron', day_of_week='mon-sun', hour=2)
# def scheduled_job():
# TODO: add parser execution here
# print('This job is run every day at 2am.')


db = intour24_database.Database()
db.connect(db_name="intour24", host="188.130.155.89", login="intour24_admin", password="R9i477o#W7cv")
if __name__ == '__main__':
    app.run(host='0.0.0.0');
