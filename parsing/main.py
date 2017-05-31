import tur_kazan
import kazantravel
# import db_model as db
# import parsing.postgre_connect as db
from postgre_connect import DBConnect, Tour
import time

if __name__ == '__main__':
    t = time.time()
    tours = kazantravel.parse()
    print(time.time() - t)
    t = time.time()
    tours.extend(tur_kazan.parse())
    print(time.time() - t)

    # db.migrate()
    database = DBConnect(db_name='intour24', user_name='intour24_admin', password='intour24_admin', host='localhost')

    print(len(tours))
    for tour in tours:
        tour.save(db=database)
    print(time.time() - t)



    # database.close()
