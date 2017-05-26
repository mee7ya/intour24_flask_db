from flask import Flask, jsonify
from flask_restful import Resource, Api
from operator import itemgetter
from nikita_first_python_program import convert
import psycopg2

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False

db = psycopg2.connect("dbname='intour24' user='intour24_admin' host='localhost' password='intour24_admin'")


class Excursions(Resource):
    def get(self):
        #parser = reqparse.RequestParser()
        #parser.add_argument('id', type=int)
        #parser.add_argument('name')
        #args = parser.parse_args()
        #constraints = 'WHERE'
        #for arg in args:
        #    if type(args[arg]) is not None:
        #        constraints += +" "+arg + "=" + args[arg]
        query = 'SELECT * FROM excursions'
        cursor = db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        rows = sorted(rows, key=itemgetter(0))
        json_response = []
        for row in rows:
            json_response.append({  'id': row[0],
                                    'name': row[1],
                                    'description': row[2],
                                    'price': row[3],
                                    'capacity': row[4],
                                    'isPicking': row[5],
                                    'startPlace': row[6],
                                    'schedule': row[7],
                                    'averageRating': row[8],
                                    'duration': convert(row[9]) })
        return jsonify(excursions=json_response)


class Sights(Resource):
    def get(self):
        query = 'SELECT * FROM sights'
        cursor = db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        rows = sorted(rows, key=itemgetter(0))
        json_response = []
        for row in rows:
            json_response.append({'id': row[0],
                                  'name': row[1],
                                  'geoposition': row[2],
                                  'images': row[3]})
        return jsonify(sights=json_response)


api.add_resource(Excursions, '/Excursions.json')
api.add_resource(Sights, '/Sights.json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True);
