import psycopg2


class Database:
    def __init__(self):
        self.db = None

    def connect(self, db_name, host, password, login):
        self.db = psycopg2.connect(
            "dbname=" + chr(39) + db_name + chr(39) +
            " user=" + chr(39) + login + chr(39) +
            " host=" + chr(39) + host + chr(39) +
            " password=" + chr(39) + password + chr(39))

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
        self.db.cursor.execute(query)
        self.db.conn.commit()

    def select_query(self, table, columns="*"):
        columns_string = ""
        for column in columns:
            columns_string += column + ', '
        columns_string = columns_string[:-2]
        query = "SELECT "+columns_string+" FROM "+table+" ORDER BY id"
        cursor = self.db.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def select_query_with_id(self, table, c_id, columns="*"):
        columns_string = ""
        for column in columns:
            columns_string += column + ', '
        columns_string = columns_string[:-2]
        query = "SELECT " + columns_string + " FROM " + table + " WHERE id=" + c_id + "ORDER BY id"
        cursor = self.db.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def select_custom_query(self, table, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        return cursor.fetchall()
