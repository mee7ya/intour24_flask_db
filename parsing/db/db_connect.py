import psycopg2


class Database:
    global db

    def connect(self, db_name, host, password, login):
        self.db = psycopg2.connect(
            "dbname='" + db_name + "' user='" + login + "' host='" + host + "' password='" + password + "")

    def insert_query(self, table, keys, values):
        key_string = ""
        for key in keys:
            key_string += key + ", "
        key_string = key_string[:-2]
        value_string = ""
        for value in values:
            value_string += value + ", "
        value_string = value_string[:-2]
        query = "INSERT INTO " + table + "(" + key_string + ") VALUES (" + value_string + ")"
        db.cursor.execute(query)
        db.conn.commit()

    def select_query(self):
        pass
