import sqlite3
from os import path
from time import time_ns


class DataBase:
    def __init__(self):
        self.con = sqlite3.connect(path.dirname(__file__) + '\\db.db')

    def _fetchall(self, query):
        cur = self.con.cursor()
        fetch = cur.execute(query).fetchall()
        cur.close()
        return fetch

    def get_modes(self):
        data = self._fetchall("SELECT * FROM modes")
        for i, row in enumerate(data):
            data[i] = [row[0]] + list(map(lambda x: (a := str(x).zfill(4))[:2] + ':' + a[2:] if x is not None else "-",
                                          row[1:]))
        return data

    def get_history(self):
        return self._fetchall("SELECT * FROM status")

    def insert_into_history(self):
        cur = self.con.cursor()
        self.con.commit()
        cur.close()


if __name__ == "__main__":
    db = DataBase()
    print('id, time, is_on')
    for i in db.get_modes():
        print(i)
