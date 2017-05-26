import psycopg2 as p


class Tour:
    def __init__(self):
        self.title = None
        self.date = None
        self.price = None
        self.time = None

    def save(self, db):
        db.cur.execute("INSERT INTO excursions (name, schedule, duration, price) VALUES ('{}', '{}', '{}', '{}');"
                       .format(self.title, self.date, self.time, self.price))
        db.conn.commit()

    # def select(self, db):
    #     db.cur.execute("SELECT name FROM excursions")
    #     result = db.cur.fetchall()
    #     print(str(result))


class DBConnect:
    def __init__(self, db_name='intour24', user_name='intour24_admin', password='intour24_admin', connect=True,
                 host='10.240.20.53'):
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

    def test_insert(self):
        self.cur.execute("INSERT INTO excursions (name, price) VALUES ('{}', '{}');".format('test', '1'))
        self.conn.commit()
