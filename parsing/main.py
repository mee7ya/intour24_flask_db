from parsing.db.postgre_connect import DBConnect
from parsing.parsers import tur_kazan_tours, kazantravel

if __name__ == '__main__':
    # database = DBConnect()
    tours = []
    tours.extend(kazantravel.parse())
    print(len(tours))
    for tour in tours:
        attrs = vars(tour)
        print(', '.join("%s: %s" % item for item in attrs.items()))
