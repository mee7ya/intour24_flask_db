import time

from parsing.db.postgre_connect import DBConnect
from parsing.parsers import kazantravel, tur_kazan_tours

if __name__ == '__main__':
    database = DBConnect()

    tours = []
    # t = time.time()
    # tours.extend(kazantravel.parse())
    t = time.time()
    tours.extend(tur_kazan_tours.parse())

    for tour in tours[0:1]:
        tour.save(database)
    database.close()
