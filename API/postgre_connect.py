import psycopg2 as p


class Excursion:
    def __init__(self):
        self.id = None
        self.name = None
        self.description = None
        self.duration = None
        self.picking_place = None
        self.price = None
        self.capacity = 50

    def save(self):
        db = DBConnect()
        db.cur.execute(
            """INSERT INTO excursions (name, description, duration, picking_place_id, price_id, capacity)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;""", (
                self.name,
                self.description,
                self.duration,
                self.picking_place,
                self.price,
                self.capacity
            )
        )
        db.conn.commit()
        self.id = db.cur.fetchone()[0]
        print("Excursion '%s' inserted by id: %s" % (self.name, self.id))
        return self.id


class ExcursionProperty:
    def __init__(self):
        self.id = None
        self.name = None
        self.icon = None

    def save(self):
        db = DBConnect()
        db.cur.execute(
            """INSERT INTO excursion_property (name, icon) 
            SELECT '{}', {}
            WHERE NOT EXISTS (SELECT name FROM excursion_property WHERE name = '{}')
            RETURNING id;
            """.format(self.name, 'NULL' if not self.icon else self.icon, self.name)
        )
        db.conn.commit()
        db.cur.execute(
            """SELECT id FROM excursion_property
            WHERE name = '{}';""".format(self.name)
        )
        db.conn.commit()
        self.id = db.cur.fetchone()[0]
        return self.id


class ExcursionExcursionProperty:
    def __init__(self):
        self.id = None
        self.excursion = None
        self.property = None

    def save(self):
        db = DBConnect()
        db.cur.execute(
            """INSERT INTO excursions_excursion_property (excursion_id, excursion_property_id)
            VALUES (%s, %s) RETURNING id""",
            (
                self.excursion, self.property
            )
        )
        db.conn.commit()
        self.id = db.cur.fetchone()[0]
        return self.id


class Sight:
    def __init__(self):
        self.id = None
        self.name = None
        self.images = None

    def save(self):
        db = DBConnect()
        db.cur.execute(
            """INSERT INTO sights (name, images) 
            SELECT '{}', {}
            WHERE NOT EXISTS (SELECT name FROM sights WHERE name = '{}')
            RETURNING id;
            """.format(self.name, 'NULL' if not self.images else self.images, self.name)
        )
        db.conn.commit()
        db.cur.execute(
            """SELECT id FROM sights
            WHERE name = '{}';""".format(self.name)
        )
        db.conn.commit()
        self.id = db.cur.fetchone()[0]
        return self.id


class ExcursionSight:
    def __init__(self):
        self.id = None
        self.excursion = None
        self.sight = None

    def save(self):
        db = DBConnect()
        db.cur.execute(
            """INSERT INTO excursions_sights (excursion_id, sight_id)
            VALUES (%s, %s) RETURNING id""",
            (
                self.excursion, self.sight
            )
        )
        db.conn.commit()
        self.id = db.cur.fetchone()[0]
        return self.id


class Schedule:
    def __init__(self):
        self.id = None
        self.excursion = None
        self.start_date = None
        self.end_date = None
        self.start_time = None
        self.everyday = None
        self.weekday = None
        self.odd_even_week = None
        self.repeat_day = None

    def save(self):
        db = DBConnect()
        db.cur.execute(
            """INSERT INTO schedule (excursion_id, start_date, end_date, start_time, 
            everyday, weekday, odd_even_week, repeat_day)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
            (
                self.excursion, self.start_date, self.end_date, self.start_time,
                self.everyday, self.weekday, self.odd_even_week, self.repeat_day
            )
        )
        db.conn.commit()
        self.id = db.cur.fetchone()[0]
        return self.id


class PickingPlace:
    def __init__(self):
        self.id = None
        self.name = None
        self.geoposition = None

    @staticmethod
    def get_place_id(start_point):
        picking_place = PickingPlace()
        picking_place.name = start_point
        picking_place.geoposition = 0
        picking_place.save()
        return picking_place.id

    def save(self):
        db = DBConnect()
        db.cur.execute(
            """INSERT INTO picking_places (name, geoposition) 
            SELECT '{}', {}
            WHERE NOT EXISTS (SELECT name FROM picking_places WHERE name = '{}')
            RETURNING id;
            """.format(self.name, 'NULL' if not self.geoposition else self.geoposition, self.name)
        )
        db.conn.commit()
        db.cur.execute(
            """SELECT id FROM picking_places
            WHERE name = '{}';""".format(self.name)
        )
        db.conn.commit()
        self.id = db.cur.fetchone()[0]
        return self.id


class Price:
    def __init__(self):
        self.id = None
        self.price_for_adult = None
        self.price_for_children = None

    @staticmethod
    def get_price_id(price_for_adult, price_for_children):
        price = Price()
        price.price_for_adult = price_for_adult
        price.price_for_children = price_for_children
        price.save()
        return price.id

    def save(self):
        db = DBConnect()
        db.cur.execute("INSERT INTO prices (price_for_children, price_for_adult) "
                            "VALUES ('{}', '{}') RETURNING id;".format(self.price_for_children,
                                                                       self.price_for_adult))
        self.id = db.cur.fetchone()[0]
        db.conn.commit()
        return self.id


class DBConnect:
    def __init__(self, db_name='intour24_test', user_name='intour24_admin', password='R9i477o#W7cv', connect=True,
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
