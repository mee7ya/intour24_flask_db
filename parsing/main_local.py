import time

import parsing.db.local_db_connect as db
from parsing.parsers import kazantravel, tur_kazan

if __name__ == '__main__':
    tours = []
    t = time.time()
    tours.extend(kazantravel.parse())
    print(time.time() - t)
    t = time.time()
    tours.extend(tur_kazan.parse())
    print(time.time() - t)

    db.migrate()

    print(len(tours))

    for tour in tours:
        tour.save()
    print(time.time() - t)
