import sqlite3
from sqlite3 import Error

DB_FILE = '//game.db'


class SqlUtil:

    @staticmethod
    def create_connection():
        conn = None
        try:
            conn = sqlite3.connect(DB_FILE)
            return conn
        except Error as e:
            print(e)

        return conn


    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


    @staticmethod
    def select_rows(conn, sql):
        conn.row_factory = SqlUtil.dict_factory
        cursor = conn.cursor()
        cursor.execute(sql)

        dict_results = []
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            dict_results.append(row)
        return dict_results


    @staticmethod
    def insert_rows(conn, sql, values):
        try:
            cursor = conn.cursor()
            cursor.execute(sql, values)
            conn.commit()
        except Error as e:
            print(e)


    @staticmethod
    def update_rows(conn, sql):
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
        except Error as e:
            print(e)
