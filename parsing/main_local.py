import time

import parsing.db.local_db_connect as db
from parsing.parsers import kazantravel, tur_kazan_tours

if __name__ == '__main__':
    tours = []
    db.migrate()

    # t = time.time()
    # tours.extend(kazantravel.parse())
    # print(time.time() - t)

    t = time.time()
    tours.extend(tur_kazan_tours.parse())

    for tour in tours:
        tour.save()
