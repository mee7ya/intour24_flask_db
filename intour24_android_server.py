from flask import Flask, url_for, request, json, Response
from nikita_first_python_program import convert
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import intour24_database


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False
schedule = BlockingScheduler()


def send_400_with_error(error):
    json_response = {'status': "ERROR",
                     'error': error}
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response, 400


@app.route('/excursion/<id>')
def excursion(id):
    if id.isdigit():
        if int(id) == 0:
            return send_400_with_error(6)
        __parameters__ = ['id', 'name', 'description', 'duration', 'priceForChildren', 'priceForAdult',
                          'priceForEnfant', 'pickingPlace', 'category', 'rating', 'properties',
                          'images']
        query = 'SELECT e.id, e.name, e.description, e.duration, p.price_for_children, p.price_for_adult, ' \
                'p.price_for_enfant, pp.name, c.name, ' \
                'e.average_rating, array_agg(DISTINCT ep.name), e.images, p.id, pp.id, c.id, array_agg(DISTINCT ep.id) ' \
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
                'GROUP BY e.id, p.price_for_children, p.price_for_adult, p.price_for_enfant, p.id, pp.id, c.id, ' \
                'pp.name, e.average_rating, c.name'
        rows = db.select_custom_query(query=query);
        if rows:
            json_price = {__parameters__[0]: rows[0][12],
                          __parameters__[4]: rows[0][4],
                          __parameters__[5]: rows[0][5],
                          __parameters__[6]: rows[0][6]
                          }
            json_picking_place = {__parameters__[0]: rows[0][13],
                                  __parameters__[1]: rows[0][7]}
            json_category = {__parameters__[0]: rows[0][14],
                             __parameters__[1]: rows[0][8]}
            json_properties = []
            for i in range(len(rows[0][15])):
                json_property = {__parameters__[0]: rows[0][15][i],
                                 __parameters__[1]: rows[0][10][i]}
                json_properties.append(json_property)
            json_response = {__parameters__[0]: rows[0][0],
                             __parameters__[1]: rows[0][1],
                             __parameters__[2]: rows[0][2],
                             __parameters__[3]: convert(rows[0][3]),
                             'price': json_price,
                             'pickingPlace': json_picking_place,
                             'category': json_category,
                             __parameters__[9]: rows[0][9],
                             'properties': json_properties,
                             __parameters__[11]: rows[0][11]}
            json_response = json.dumps(json_response)
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response
        else:
            return send_400_with_error(2)
    else:
        try:
            if int(id) < 0:
                return send_400_with_error(6)
        except ValueError:
            return send_400_with_error(5)


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
        if int(id) == 0:
            return send_400_with_error(6)
        __parameters__ = ['id', 'name', 'geoposition', 'images', 'description', 'cover', 'properties', 'excursions']
        query = 'SELECT s.*, array_agg(DISTINCT sp.name), array_agg(DISTINCT sp.image) ' \
                'FROM sights s ' \
                'LEFT JOIN sights_sight_property ssp ' \
                'ON s.id = ssp.sight_id ' \
                'LEFT JOIN sight_property sp ' \
                'ON ssp.sight_property_id = sp.id ' \
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
                             __parameters__[6]: properties}
            json_response = json.dumps(json_response)
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response
        else:
            return send_400_with_error(2)
    else:
        try:
            if int(id) < 0:
                return send_400_with_error(6)
        except ValueError:
            return send_400_with_error(5)


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
    group_id = request.form.get('group_id')
    seats_reserved = request.form.get('seats_reserved');
    if not (group_id == '' or seats_reserved == ''):
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
                                     'group_id': int(group_id),
                                     'seats_reserved': more_seats_reserved}
                else:
                    json_response = {'status': "OK",
                                     'full': 0,
                                     'group_id': int(group_id),
                                     'seats_reserved': more_seats_reserved}
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
    __parameters_group__ = ['id', 'tour_date', 'seats_reserved', 'guide_id', 'seats_capacity', 'excursion']
    __parameters_excursion__ = ['id', 'name', 'description', 'capacity', 'average_rating', 'duration', 'linkToSite',
                                'images', 'category', 'picking_place', 'price', 'properties', 'sight']
    __parameters_category__ = ['id', 'name']
    __parameters_picking_place__ = ['id', 'name', 'geoposition']
    __parameters_price__ = ['id', 'price_for_children', 'price_for_adult', 'price_for_enfant']
    __parameters_properties__ = ['id', 'name', 'image']
    __parameters_sight__ = ['id', 'name']
    if date is not None and sight_id is not None:
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return send_400_with_error(4)
        if not sight_id.isdigit():
            try:
                if int(sight_id) < 0:
                    return send_400_with_error(6)
            except ValueError:
                return send_400_with_error(5)
        if int(sight_id) == 0:
                return send_400_with_error(6)
        where_clause = "WHERE g.tour_date::date = '"+date+"' AND s.id = "+sight_id
    else:
        return send_400_with_error(1)
    query = 'SELECT g.id, g.tour_date, g.seats_reserved, g.guide_id, g.seats_capacity, e.id, e.name, e.description, ' \
            'e.capacity, e.average_rating, e.duration, e.link_to_site, e.images, ' \
            'c.*, p.*, pp.*, array_agg(ep.id), array_agg(ep.name), array_agg(ep.icon), s.id, s.name ' \
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
                                  __parameters_group__[1]: str(row[1]),
                                  __parameters_group__[2]: row[2],
                                  __parameters_group__[3]: row[3],
                                  __parameters_group__[4]: row[4],
                                  __parameters_group__[5]: json_excursion,
                                  })
        json_response = json.dumps(json_response)
        response = Response(json_response, content_type='application/json; charset=utf-8')
        return response
    else:
        return send_400_with_error(2)


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

@app.route('/group/<sight_id>')
def group(sight_id):
    __parameters_group__ = ['id', 'tour_date', 'seats_reserved', 'guide_id', 'seats_capacity', 'excursion']
    __parameters_excursion__ = ['id', 'name', 'description', 'capacity', 'average_rating', 'duration', 'linkToSite',
                                'images', 'category', 'picking_place', 'price', 'properties', 'sight', 'operator']
    __parameters_category__ = ['id', 'name']
    __parameters_picking_place__ = ['id', 'name', 'geoposition']
    __parameters_price__ = ['id', 'price_for_children', 'price_for_adult', 'price_for_enfant']
    __parameters_properties__ = ['id', 'name', 'image']
    __parameters_sight__ = ['id', 'name']
    __parameters_operator__ = ['id', 'name', 'phone', 'address', 'logo', 'accreditation']
    if sight_id is not None:
        try:
            if int(sight_id) <= 0:
                return send_400_with_error(6)
        except ValueError:
            return send_400_with_error(5)
        query = 'SELECT g.id, g.tour_date, g.seats_reserved, g.guide_id, g.seats_capacity, e.id, e.name, e.description, ' \
                'e.capacity, e.average_rating, e.duration, e.link_to_site, e.images, ' \
                'c.*, p.*, pp.*, array_agg(ep.id), array_agg(ep.name), array_agg(ep.icon), s.id, s.name, o.* ' \
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
                'WHERE g.id = '+sight_id+' ' \
                'GROUP BY g.id, e.id, c.id, p.id, pp.id, s.id, o.id ' \
                'ORDER BY g.id;'
        rows = db.select_custom_query(query=query)
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
    else:
        return send_400_with_error(1)


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


@app.route('/bookings/', methods=['POST'])
def bookingsAdd():
    group_id = request.form.get('group_id')
    tourist_id = request.form.get('tourist_id')
    adults = request.form.get('adults')
    children = request.form.get('children')
    enfants = request.form.get('enfants')
    create_datetime = request.form.get('create_datetime')
    total_price = request.form.get('total_price')
    if not (group_id == '' or tourist_id == '' or adults == '' or children == '' or enfants == '' or
            create_datetime == '' or total_price == ''):
        try:
            datetime.datetime.strptime(create_datetime, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return send_400_with_error(4)
        try:
            if int(group_id) <= 0 or int(tourist_id) <= 0 or int(adults) < 0 or \
                            int(children) < 0 or int(enfants) < 0 or int(total_price) <= 0:
                return send_400_with_error(6)
        except ValueError:
            return send_400_with_error(5)
        query = "INSERT INTO bookings(tourist_id, group_id, adults, children, " \
                "enfants, total_price, create_datetime, is_cancelled) " \
                "VALUES ("+tourist_id+", "+group_id+", "+adults+", "+children+", "+enfants+", "+total_price+", '"+create_datetime+"', 0) " \
                "RETURNING id; "
        c_id = db.update_insert_custom_query(query)
        json_response = {'status': 'OK',
                         'id': c_id}
        json_response = json.dumps(json_response)
        response = Response(json_response, content_type='application/json; charset=utf-8')
        return response
    else:
        return send_400_with_error(1)


@app.route('/bookingsByTouristId/<tourist_id>')
def bookings(tourist_id):
    if tourist_id is not None:
        if tourist_id.isdigit():
            if int(tourist_id) == 0:
                return send_400_with_error(6)
            __parameters_booking__ = ['id', 'excursion', 'total_price', 'payment_id', 'group']
            __parameters_excursion__ = ['id', 'name', 'picking_place', 'duration']
            __parameters_picking_place__ = ['id', 'name']
            __parameters_group__ = ['id', 'tour_date']
            query = "SELECT b.id, b.total_price, p.id, e.id, e.name, e.duration, pp.id, pp.name, g.id, g.tour_date " \
                    "FROM bookings b " \
                    "LEFT JOIN payments p " \
                    "ON b.id = p.booking_id " \
                    "LEFT JOIN groups g " \
                    "ON b.group_id = g.id " \
                    "LEFT JOIN excursions e " \
                    "ON g.excursion_id = e.id " \
                    "LEFT JOIN picking_places pp " \
                    "ON e.picking_place_id = pp.id " \
                    "WHERE b.tourist_id =  " +tourist_id + \
                    "GROUP BY b.id, p.id, pp.id, g.id, e.id " \
                    "ORDER BY b.id "
            rows = db.select_custom_query(query)
            if rows:
                json_response = []
                for row in rows:
                    json_picking_place = {__parameters_picking_place__[0]: row[6],
                                          __parameters_picking_place__[1]: row[7]}
                    json_group = {__parameters_group__[0]: row[8],
                                  __parameters_group__[1]: str(row[9])}
                    json_excursion = {__parameters_excursion__[0]: row[3],
                                      __parameters_excursion__[1]: row[4],
                                      __parameters_excursion__[2]: json_picking_place,
                                      __parameters_excursion__[3]: convert(row[5])}
                    json_response.append({__parameters_booking__[0]: row[0],
                                          __parameters_booking__[1]: json_excursion,
                                          __parameters_booking__[2]: row[1],
                                          __parameters_booking__[3]: row[2],
                                          __parameters_booking__[4]: json_group})
                json_response = json.dumps(json_response)
                response = Response(json_response, content_type='application/json; charset=utf-8')
                return response
            else:
                return send_400_with_error(2)
        try:
            if int(tourist_id) < 0:
                return send_400_with_error(6)
        except ValueError:
            return send_400_with_error(5)
    return send_400_with_error(1)


@app.route('/booking/<id>')
def booking(id):
    if id is not None:
        if id.isdigit():
            if int(id) == 0:
                return send_400_with_error(6)
            __parameters__ = ['id', 'adults', 'children', 'enfants', 'total_price', 'group']
            __parameters_group__ = ['id', 'tour_date', 'excursion']
            __parameters_excursion__ = ['id', 'name', 'duration', 'operator', 'picking_place', 'properties']
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
                    'WHERE b.id = ' + id + \
                    'GROUP BY b.id, g.id, e.id, o.id, pp.id ' \
                    'ORDER BY b.id '
            rows = db.select_custom_query(query)
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
        try:
            if int(id) < 0:
                return send_400_with_error(6)
        except ValueError:
            return send_400_with_error(5)
    return send_400_with_error(1)


@app.route('/payments/', methods=['POST'])
def paymentsAdd():
    booking_id = request.form.get('booking_id')
    payment_time = request.form.get('payment_time')
    identifier = request.form.get('identifier')
    if booking_id != '' and payment_time != '' and identifier != '':
        try:
            datetime.datetime.strptime(payment_time, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return send_400_with_error(4)
        try:
            if int(booking_id) <= 0:
                return send_400_with_error(6)
        except ValueError:
            return send_400_with_error(5)

        query = "INSERT INTO payments (booking_id, create_datetime, is_cancelled, is_refund) " \
                "VALUES ("+booking_id+", '"+payment_time+"', 0, 0) " \
                "RETURNING id;"
        c_id = db.update_insert_custom_query(query)
        json_response = {'status': "OK",
                         'payment_id': c_id,
                         'create_datetime': payment_time}
        json_response = json.dumps(json_response)
        response = Response(json_response, content_type='application/json; charset=utf-8')
        return response
    else:
        return send_400_with_error(1)


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


@app.route('/checkPhone/<phone>')
def check_phone(phone):
    if phone != '':
        if phone.isdigit():
            if len(phone) > 20:
                return send_400_with_error(6)
            query = "SELECT id FROM tourists WHERE phone='"+phone+"' "
            rows = db.select_custom_query(query)
            if rows:
                json_response = {"status": 1}
            else:
                json_response = {"status": 0}
            json_response = json.dumps(json_response)
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response
        else:
            return send_400_with_error(5)
    else:
        return send_400_with_error(1)


@app.route('/registration', methods=['POST'])
def registration():
    name = request.form.get('name')
    phone = request.form.get('phone')
    if name != '' and phone != '':
        if len(name) > 60 or len(phone) > 20:
            return send_400_with_error(6)
        if phone.isdigit():
            query = "INSERT INTO tourists (first_name, phone) " \
                    "SELECT '"+name+"', '"+phone+"' " \
                    "WHERE NOT EXISTS (SELECT id FROM tourists WHERE phone = '"+phone+"')" \
                    "RETURNING id;"
            c_id = db.update_insert_custom_query_if_not_exists(query)
            if c_id is not None:
                json_response = {"status": "OK",
                                 "id": +c_id[0]}
                json_response = json.dumps(json_response)
                response = Response(json_response, content_type='application/json; charset=utf-8')
                return response
            else:
                return send_400_with_error(2)
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
    if c_id != '' and name != '' and phone != '':
        if len(name) > 60 or len(phone) > 20:
            return send_400_with_error(6)
        try:
            if int(c_id) <= 0 or int(phone) <= 0:
                return send_400_with_error(6)
        except ValueError:
            return send_400_with_error(5)
        query = "UPDATE tourists SET first_name = '"+name+"', phone = '"+phone+"' WHERE id="+c_id+"RETURNING id;"
        c_id = db.update_insert_custom_query_if_not_exists(query)
        if c_id is not None:
            json_response = {"status": "OK",
                             "id": c_id[0]}
            json_response = json.dumps(json_response)
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response
        else:
            return send_400_with_error(2)
    return send_400_with_error(1)


@app.route('/cancelPayment', methods=['PUT'])
def cancel_payment():
    booking_id = request.form.get('booking_id')
    if booking_id != '':
        if booking_id.isdigit():
            if int(booking_id) == 0:
                return send_400_with_error(6)
            query = 'UPDATE payments SET is_cancelled = 1 WHERE booking_id = '+booking_id+'RETURNING id'
            payment_id = db.update_insert_custom_query_if_not_exists(query)
            if payment_id is not None:
                query = 'UPDATE bookings SET is_cancelled = 1 WHERE id = '+booking_id+'RETURNING id'
                booking_id = db.update_insert_custom_query_if_not_exists(query)
                json_response = {"status": "OK",
                                 "payment_id": payment_id[0],
                                 "booking_id": booking_id[0]}
                json_response = json.dumps(json_response)
                response = Response(json_response, content_type='application/json; charset=utf-8')
                return response
            json_response = {'status': 'ERROR',
                             'error': 1}
            json_response = json.dumps(json_response)
            response = Response(json_response, content_type='application/json; charset=utf-8')
            return response, 400
        else:
            try:
                if int(booking_id) < 0:
                    return send_400_with_error(6)
            except ValueError:
                return send_400_with_error(5)
    return send_400_with_error(1)


@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='favicon.ico')


# @schedule.scheduled_job('cron', day_of_week='mon-sun', hour=2)
# def scheduled_\job():
# TODO: add parser execution here
# print('This job is run every day at 2am.')


db = intour24_database.Database()
db.connect(db_name="intour24", host="188.130.155.89", login="intour24_admin", password="R9i477o#W7cv")
if __name__ == '__main__':
    app.run(host='0.0.0.0');
