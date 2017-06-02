from flask import Flask, jsonify, url_for
from flask_restful import reqparse
from nikita_first_python_program import convert
from apscheduler.schedulers.blocking import BlockingScheduler
import intour24_database

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
schedule = BlockingScheduler()


@app.route('/excursions')
def excursions():
    __parameters__ = ['id', 'name', 'description', 'capacity', 
                      'averageRating', 'duration', 'categoryId', 'startPlaceId',                      'operatorId', 'link_to_site', 'images', 'priceId']
    __table__ = 'excursions'
    # parser = reqparse.RequestParser()
    # parser.add_argument(__parameters__[0], type=int)
    # parser.add_argument(__parameters__[1])
    # parser.add_argument(__parameters__[2])
    # parser.add_argument(__parameters__[3], type=int)
    # parser.add_argument(__parameters__[4])
    # parser.add_argument(__parameters__[5])
    # parser.add_argument(__parameters__[6])
    # parser.add_argument(__parameters__[7])
    # parser.add_argument(__parameters__[8])
    # parser.add_argument(__parameters__[9])
    # args = parser.parse_args()
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
                              __parameters__[11]: row[11],
                            })
    return jsonify(json_response)


@app.route('/sights')
def sights():
    __table__ = 'sights'
    __parameters__ = ['id', 'name', 'geoposition', 'images', 'description', 'cover']
    rows = db.select_query(table=__table__)
    json_response = []
    for row in rows:
        json_response.append({__parameters__[0]: row[0],
                              __parameters__[1]: row[1],
                              __parameters__[2]: row[2],
                              __parameters__[3]: row[3],
                              __parameters__[4]: row[4],
                              __parameters__[5]: row[5]})
    return jsonify(json_response)


@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='favicon.ico')

@app.route('/')
def ap2():
    return "API"
    


@schedule.scheduled_job('cron', day_of_week='mon-sun', hour=2)
def scheduled_job():
    # TODO: add parser execution here
    print('This job is run every day at 2am.')


db = intour24_database.Database()
db.connect(db_name="intour24", host="localhost", login="intour24_admin", password="R9i477o#W7cv")
if __name__ == '__main__':
    app.run();
