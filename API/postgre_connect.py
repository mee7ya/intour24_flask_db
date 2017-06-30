import psycopg2 as p


class Sight:
    def __init__(self):
        self.id = None
        self.name = None
        self.images = None
        self.db = DBConnect()

    def save(self):
        self.db.cur.execute(
            """
            INSERT INTO sights (name, images) 
            SELECT '{}', {}
            WHERE NOT EXISTS (SELECT name FROM sights WHERE name = '{}')
            RETURNING id;
            """.format(self.name, 'NULL' if not self.images else self.images, self.name)
        )
        self.db.conn.commit()
        self.db.cur.execute(
            """
            SELECT id FROM sights
            WHERE name = '{}';
            """.format(self.name)
        )
        self.db.conn.commit()
        self.id = self.db.cur.fetchone()[0]
        return self.id


class ExcursionProperty:
    def __init__(self):
        self.id = None
        self.name = None
        self.icon = None
        self.db = DBConnect()

    def save(self):
        self.db.cur.execute(
            "INSERT INTO excursion_property (name, icon) "
            "VALUES ('{}', '{}') RETURNING id;".format(self.name, self.icon
                                                       )
        )
        self.db.conn.commit()
        self.id = self.db.cur.fetchone()[0]
        return self.id


class Schedule:
    def __init__(self):
        self.id = None
        self.start_date = None
        self.excursion = None
        self.end_date = None
        self.repeat_interval = 0
        self.repeat_day = None
        self.repeat_month = None
        self.repeat_week = None
        self.repeat_weekday = None
        self.db = DBConnect()

    def save(self):
        self.db.cur.execute(
            "INSERT INTO schedule (start_date, excursion_id, end_date, repeat_interval, "
            "repeat_day, repeat_month, repeat_week, repeat_weekday) "
            "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}') RETURNING id;".format(
                self.start_date, self.excursion, self.end_date, self.repeat_interval,
                self.repeat_day, self.repeat_month, self.repeat_week, self.repeat_weekday
            )
        )
        self.db.conn.commit()
        self.id = self.db.cur.fetchone()[0]
        return self.id


class PickingPlace:
    def __init__(self):
        self.id = None
        self.name = None
        self.geoposition = None
        self.db = DBConnect()

    @staticmethod
    def get_place_id(start_point):
        picking_place = PickingPlace()
        picking_place.name = start_point
        picking_place.geoposition = 0
        picking_place.save()
        return picking_place.id

    def save(self):
        self.db.cur.execute("INSERT INTO picking_places (name, geoposition)"
                            "VALUES ('{}', '{}') RETURNING id;".format(self.name, self.geoposition))
        self.id = self.db.cur.fetchone()[0]
        self.db.conn.commit()


class Price:
    def __init__(self):
        self.id = None
        self.price_for_adult = None
        self.price_for_children = None
        self.db = DBConnect()

    @staticmethod
    def get_price_id(price_for_adult, price_for_children):
        price = Price()
        price.price_for_adult = price_for_adult
        price.price_for_children = price_for_children
        price.save()
        return price.id

    def save(self):
        self.db.cur.execute("INSERT INTO prices (price_for_children, price_for_adult) "
                            "VALUES ('{}', '{}') RETURNING id;".format(self.price_for_children,
                                                                       self.price_for_adult))
        self.id = self.db.cur.fetchone()[0]
        self.db.conn.commit()


class Excursion:
    def __init__(self):
        self.id = None
        self.name = None
        self.description = None
        self.duration = None
        self.picking_place = None
        self.price = None
        self.db = DBConnect()

    def save(self):
        self.db.cur.execute(
            "INSERT INTO excursions (name, description, duration) "
            "VALUES ('{}', '{}', '{}') RETURNING id;".format(
                self.name,
                self.description,
                self.duration
            )
        )

        self.db.conn.commit()
        self.id = self.db.cur.fetchone()[0]


class DBConnect:
    def __init__(self, db_name='intour24', user_name='intour24_admin', password='R9i477o#W7cv', connect=True,
                 host='188.130.155.89'):
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
