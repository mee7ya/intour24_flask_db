import psycopg2 as p


class Dates:
    def __init__(self):
        self.start_date = None
        self.repeat_interval = None
        self.excursion_id = None

    def get_dates_id(self, start_date, repeat_interval):
        dates = Dates()
        dates.start_date = start_date
        dates.repeat_interval = repeat_interval
        dates.save()
        return dates.id

    def save(self):
        db = DBConnect()
        db.cur.execute("INSERT INTO schedule (start_date, repeat_interval, excursion_id) "
                            "VALUES ('{}', '{}', '{}');".format(self.start_date, self.repeat_interval,
                                                                self.excursion_id))
        db.conn.commit()
        db.close()


class PickingPlace:
    def __init__(self):
        self.name = None
        self.geoposition = None
        self.id = None

    def get_place_id(start_point):
        picking_place = PickingPlace()
        picking_place.name = start_point[0]
        picking_place.geoposition = start_point[1]
        picking_place.save()
        return picking_place.id

    def save(self):
        db = DBConnect()
        db.cur.execute("INSERT INTO picking_places (name, geoposition)"
                            "VALUES ('{}', '{}') RETURNING id;".format(self.name, self.geoposition))
        self.id = self.db.cur.fetchone()[0]
        db.conn.commit()
        db.close()


class Price:
    def __init__(self):
        self.price_for_adult = None
        self.price_for_children = None
        self.price_for_enfant = None
        self.id = None

    def get_price_id(prices):
        price = Price()
        price.price_for_adult = prices[0]
        price.price_for_children = prices[1]
        price.price_for_enfant = prices[2]
        price.save()
        return price.id

    def save(self):
        db = DBConnect()
        db.cur.execute("INSERT INTO prices (price_for_children, price_for_adult, price_for_enfant) "
                            "VALUES ('{}', '{}', '{}') RETURNING id;".format(self.price_for_children,
                                                                             self.price_for_adult,
                                                                             self.price_for_enfant))
        self.id = self.db.cur.fetchone()[0]
        db.conn.commit()
        db.close()



class Tour:
    def __init__(self):
        self.title = None
        self.price_id = None
        self.duration = None
        self.description = None
        self.start_point = None
        self.id = None

    def save(self):
        db = DBConnect()
        db.cur.execute("INSERT INTO excursions (name, duration, price_id, description, picking_place_id) "
                            "VALUES ('{}', '{}', '{}', '{}', '{}') RETURNING id;".format(self.title, self.duration,
                                                                                         self.price_id,
                                                                                         self.description,
                                                                                         self.start_point))
        self.id = self.db.cur.fetchone()[0]
        db.conn.commit()
        db.close()


class DBConnect:
    def __init__(self, db_name='intour24_test', user_name='intour24_admin', password='R9i477o#W7cv', connect=True,
                 host='localhost'):
        self.PARAMS = "dbname='{}' user='{}' password='{}' host={}".format(db_name, user_name, password, host)
        self.conn = None
        self.cur = None
        if connect:
            self.connect()

    def connect(self):
        self.conn = p.connect(self.PARAMS)
        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()
