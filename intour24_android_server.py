from flask import Flask, jsonify, url_for
from flask_restful import Resource, Api, reqparse
from nikita_first_python_program import convert
import intour24_database as db

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False


class Excursions(Resource):
    def get(self):
        PARAMETERS = ['id', 'name', 'description', 'price', 'capacity', 'isPicking',
                      'startPlace', 'schedule', 'averageRating', 'duration']
        TABLE = 'excursions'
        parser = reqparse.RequestParser()
        parser.add_argument(PARAMETERS[0], type=int)
        parser.add_argument(PARAMETERS[1])
        parser.add_argument(PARAMETERS[2])
        parser.add_argument(PARAMETERS[3], type=int)
        parser.add_argument(PARAMETERS[4])
        parser.add_argument(PARAMETERS[5])
        parser.add_argument(PARAMETERS[6])
        parser.add_argument(PARAMETERS[7])
        parser.add_argument(PARAMETERS[8])
        parser.add_argument(PARAMETERS[9])
        args = parser.parse_args()
        args_are_empty = 1
        for arg in args:
            if args[arg] != None:
                args_are_empty = 0
                break
        if args_are_empty == 1:
            rows = db.select_query(TABLE, "*")
        else:
            rows = db.select_query(TABLE, "*", args)
        json_response = []
        for row in rows:
            json_response.append({PARAMETERS[0]: row[0],
                                  PARAMETERS[1]: row[1],
                                  PARAMETERS[2]: row[2],
                                  PARAMETERS[3]: row[3],
                                  PARAMETERS[4]: row[4],
                                  PARAMETERS[5]: row[5],
                                  PARAMETERS[6]: row[6],
                                  PARAMETERS[7]: row[7],
                                  PARAMETERS[8]: row[8],
                                  PARAMETERS[9]: convert(row[9])})
        return jsonify(excursions=json_response)


class Sights(Resource):
    def get(self):
        rows = db.select_query("sights", "*")
        json_response = []
        for row in rows:
            json_response.append({'id': row[0],
                                  'name': row[1],
                                  'geoposition': row[2],
                                  'images': row[3]})
        return jsonify(sights=json_response)


api.add_resource(Excursions, '/Excursions.json')
api.add_resource(Sights, '/Sights.json')
# app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))

db.connect(db_name="intour24", host="localhost", login="intour24_admin", password="intour24_admin")
# db = psycopg2.connect("dbname='intour24' user='intour24_admin' host='localhost' password='intour24_admin'")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True);
