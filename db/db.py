import sqlite3
from os import path
from time import time_ns


class DataBase:
    def __init__(self):
        self.con = sqlite3.connect(path.dirname(__file__) + '\\db.db')

    def get_all(self):
        cur = self.con.cursor()
        fetch = cur.execute("SELECT * FROM status").fetchall()
        cur.close()
        return fetch

    def insert(self):
        cur = self.con.cursor()

        self.con.commit()
        cur.close()


if __name__ == "__main__":
    db = DataBase()
    print(time_ns())
    print('id, time, is_on')
    for i in db.get_all():
        print(i)
