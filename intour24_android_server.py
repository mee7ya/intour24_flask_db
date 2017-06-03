from flask import Flask, jsonify, url_for, request, json, Response
from flask_restful import reqparse
from nikita_first_python_program import convert
from apscheduler.schedulers.blocking import BlockingScheduler
import intour24_database

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False
schedule = BlockingScheduler()


@app.route('/excursions')
def excursions():
    __parameters__ = ['id', 'name', 'description', 'capacity',
                      'averageRating', 'duration', 'categoryId', 'startPlaceId', 'operatorId', 'link_to_site', 'images',
                      'priceId']
    __table__ = 'excursions'
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
                                  __parameters__[5]: convert(row[5]),
                                  __parameters__[6]: row[6],
                                  __parameters__[7]: row[7],
                                  __parameters__[8]: row[8],
                                  __parameters__[9]: row[9],
                                  __parameters__[10]: row[10],
                                  __parameters__[11]: row[11]
                                  })
    else:
        __parameters__ = ['id', 'name', 'description', 'duration', 'priceForChildren', 'priceForAdult',
                          'priceForEnfant', 'pickingPlace', 'category', 'rating', 'properties', 'schedule',
                          'images']
        query = 'SELECT e.id, e.name, e.description, e.duration, p.price_for_children, p.price_for_adult, ' \
                'p.price_for_enfant, pp.name, c.name, ' \
                'e.average_rating, array_agg(ep.name), array_agg(s.start_date), e.images '\
                'FROM excursions e '\
                'LEFT JOIN prices p '\
                'ON e.price_id = p.id '\
                'LEFT JOIN picking_places pp '\
                'ON e.picking_place_id = pp.id '\
                'LEFT JOIN category c '\
                'ON e.category_id = c.id '\
                'LEFT JOIN excursions_excursion_property eep '\
                'ON e.id = eep.excursion_id '\
                'LEFT JOIN excursion_property ep '\
                'ON ep.id = eep.excursion_property_id '\
                'LEFT JOIN schedule s '\
                'ON s.excursion_id = e.id '\
                'WHERE e.id =  '+c_id+ \
                'GROUP BY e.id, p.price_for_children, p.price_for_adult, p.price_for_enfant, ' \
                'pp.name, e.average_rating, c.name'
        rows = db.select_custom_query(table=__table__, query=query);
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
                         __parameters__[11]: rows[0][11],
                         __parameters__[12]: rows[0][12]}
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


@app.route('/sights')
def sights():
    __table__ = 'sights'
    __parameters__ = ['id', 'name', 'geoposition', 'images', 'description', 'cover']
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


@app.route('/groups')
def groups():
    __table__ = 'groups'
    __parameters__ = ['id', 'tour_date', 'seats_reserved', 'excursions_id', 'guide_id',
                      'seats_capacity']
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


@app.route('/prices')
def prices():
    __table__ = 'prices'
    __parameters__ = ['id', 'price_for_children', 'price_for_adult', 'price_for_enfant']
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
                         __parameters__[3]: rows[0][3]}
    json_response = json.dumps(json_response)
    response = Response(json_response, content_type='application/json; charset=utf-8')
    return response


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
