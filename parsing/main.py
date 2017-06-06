from parsing.db.postgre_connect import DBConnect
from parsing.parsers import tur_kazan_tours

if __name__ == '__main__':
    # database = DBConnect()
    tours = []
    tours.extend(tur_kazan_tours.parse())
    print(len(tours))
