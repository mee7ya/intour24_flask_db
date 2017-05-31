import psycopg2 as p


class Tour:
    def __init__(self):
        self.title = None
        self.date = None
        self.price = None
        self.time = None

    def save(self, db):
        quesry = "INSERT INTO excursions (name, schedule, duration, price) VALUES (" + chr(39) + self.title + chr(39) \
                 +", " + chr(39) + self.date + chr(39) + ", " + chr(39) + self.time + chr(39) + ", " + self.price + ")"
        db.cur.execute(quesry)
        db.conn.commit()


class DBConnect:
    def __init__(self, db_name, user_name, password, connect=True, host=None):
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
