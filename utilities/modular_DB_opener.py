import sqlite3

class Opener:

    def __init__(self, name):
        self.CONN = sqlite3.connect(f"{name}.db")
        self.CUR = self.CONN.cursor()
        self.CUR.execute("SELECT * FROM all_tables ")
        tables = self.CUR.fetchall()

    def GetData(self, table, parameter):
        command = f"SELECT * FROM {table} WHERE {parameter}"
        self.CUR.execute(command)
        return self.CUR.fetchall()