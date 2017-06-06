import psycopg2 as p


class Tour:
    def __init__(self):
        self.title = None
        self.schedule = None
        self.price = None
        self.duration = None
        self.description = None
        self.start_point = None
        self.id = None

    def save(self, db):
        db.cur.execute("INSERT INTO excursions (name, schedule, duration, price_id, description, picking_place_id) "
                       "VALUES ('{}', '{}', '{}', '{}', '{}', '{}');"
                       .format(self.title, self.schedule, self.duration, self.price, self.description,
                               self.start_point))
        db.conn.commit()


class Price:
    def __init__(self):
        self.id = None
        self.price_for_adult = None
        self.price_for_children = None
        self.price_for_enfant = None

    @staticmethod
    def get_price_id(price_for_adult, price_for_children, price_for_enfant):
        price = Price()
        price.price_for_adult = price_for_adult
        price.price_for_children = price_for_children
        price.price_for_enfant = price_for_enfant
        # price.save()
        return price.id

    def save(self, db):
        db.cur.execute(
            "INSERT INTO prices (price_for_adult, price_for_children, price_for_enfant)" +
            " VALUES ('{}', '{}', '{}');"
            .format(self.price_for_adult, self.price_for_children, self.price_for_enfant))
        db.conn.commit()
        db.cur.execute(
            "SELECT id FROM prices WHERE " +
            "price_for_adult == '{}' AND price_for_children == '{}' AND price_for_enfant == '{}';"
            .format(self.price_for_adult, self.price_for_children, self.price_for_enfant))
        self.id = db.cur.fetchone()[0]


class PickingPlace:
    def __init__(self):
        self.id = None
        self.name = None
        self.geoposition = None

    @staticmethod
    def get_place_id(name, geoposition):
        picking_place = PickingPlace()
        picking_place.name = name
        picking_place.geoposition = geoposition
        # picking_place.save()
        return picking_place.id

    def save(self, db):
        db.cur.execute(
            "INSERT INTO Picking_place WHERE" +
            "name == '{}' AND geoposition == '{}' RETURNING id;"
            .format(self.name, self.geoposition))
        self.id = db.cur.fetchone()[0]


class Dates:
    def __init__(self):
        self.start_date = None
        self.repeat_interval = None
        self.excursion_id = None

    @staticmethod
    def get_dates_id(start_date, repeat_interval):
        dates = Dates()
        dates.start_date = start_date
        dates.repeat_interval = repeat_interval
        # dates.save()
        return dates.id

    def save(self, db):
        db.cur.execute(
            "INSERT INTO Schedule WHERE" +
            "start_date == '{}' AND repeat_interval == '{}' AND excursion_id == '{}';"
            .format(self.start_date, self.repeat_interval, self.excursion_id))
        # self.id = db.cur.fetchone()[0]


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
