import time

from parsing.db.postgre_connect import DBConnect
from parsing.parsers import kazantravel, tur_kazan

if __name__ == '__main__':
    database = DBConnect()

    tours = []
    t = time.time()
    tours.extend(kazantravel.parse())
    print(time.time() - t)
    t = time.time()
    tours.extend(tur_kazan.parse())
    print(time.time() - t)

    for tour in tours[0:1]:
        tour.save(database)
    print(time.time() - t)
    database.close()
