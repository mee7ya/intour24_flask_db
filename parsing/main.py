from parsing import tur_kazan
from parsing import kazantravel
import parsing.db_model as db
# import parsing.postgre_connect as db
from parsing.postgre_connect import DBConnect
import time

if __name__ == '__main__':
    tours = []
    t = time.time()
    tours.extend(kazantravel.parse())
    print(time.time() - t)
    t = time.time()
    tours.extend(tur_kazan.parse())
    print(time.time() - t)

    db.migrate()
    # database = DBConnect('dbafp', 'user', 'pass')

    print(len(tours))

    for tour in tours:
        tour.save()
    print(time.time() - t)

    # database.close()
