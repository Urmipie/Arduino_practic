import sqlite3
from os import path


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

    def add_mode(self, mode: tuple):
        cur = self.con.cursor()
        cur.execute('INSERT INTO modes(time_on, time_off) VALUES (?, ?)', mode)
        self.con.commit()
        cur.close()

    def delete_mode(self, id_):
        cur = self.con.cursor()
        cur.execute(f'DELETE FROM modes WHERE ID = {id_}')
        self.con.commit()
        cur.close()
