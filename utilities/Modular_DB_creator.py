import sqlite3


# PRIMARNI TABLE - sve sto se moze naci sa search
# Prvo sve feedat u dict tj oblik: string - [ID/NES/NES/NES,ID/NES/NES/NES,ID/NES]
# Possible /SNO, /SGE, /SDA, /SAC, /SAB, /SVO - ako vise na isti ID - STACK! - id = 6 znamenki
# NA KRAJU: TABLE  Ime: Blabla CorrespondsTo: List FetchID: #AADBS - proceduralno generiran

# SEKUNDARNI TABLE - baza type ID i corr. veze i assembly mode
# Assembly mode
# 0: Nema dekl.
# 1: Ima Dekl - SP
# 2: Ima Dekl: S
# 3. Ima Dekl - P

# THIRD TABLE - podaci - povezan pomocu ID- tj ID rod tip dekl. i description
#

# NPR: T 2
# abactio noun 954438 #AADBS#OONDF#ACIFD#FBEBD 1


# MANUAL - Assembler - Init - ako nece datawipe, dodati parameter "NO"
#                             create_tables: za sada po 1 table i values u listi za taj tables, FUTURE - more tables
#                             Add_to_table: Specificirat koji table i dat tocno vals, inace error
#                             FetchAllTables: Tocno to - vraca tuple, specificnije - (TABLE, (VALUES))
#                             ResetDB - zamisljeno kao internal Funkcija - moze se koristiti kao except, ako table=init

class Assembler:

    def __init__(self, name, mode="w"):
        self.CONN = sqlite3.connect(f"{name}.db")
        self.CURS = self.CONN.cursor()
        command = f"CREATE TABLE IF NOT EXISTS all_tables (table_name TEXT PRIMARY KEY)"
        self.CURS.execute(command)
        self.AllTables = {}
        if mode == "w":
            self.ResetDB()
        print("initialized!")

    def __buildTable(self,table, values_for_table):
        command2 = f"CREATE TABLE IF NOT EXISTS {table} ("
        for i in range(len(values_for_table)):
            command2 += values_for_table[i] + ", "
        command2 = command2[:-2] + ")"
        self.CURS.execute(command2)
        try:
            self.CURS.execute("INSERT INTO all_tables VALUES (?)", [table])
            self.AllTables[table] = values_for_table
        except:
            raise BaseException("Something is wrong!")
        self.CONN.commit()

    def create_tables(self, tables: list or str, values_for_tables: list):
        if tables.__class__ == str:
            self.__buildTable(tables, values_for_tables)

        elif tables.__class__ == list:
            for iterator in range(len(tables)):
                self.__buildTable(tables[iterator], values_for_tables[iterator])


    def AddToTable(self, table, add, many=False):
        if not many:
            x = ""
            for i in range(len(add)): x += "?, "

            command = f"insert into {table} values ({x[:-2]})"
            self.CURS.execute(command, add)
            self.CONN.commit()

    def FetchAllTables(self):
        if tuple(self.AllTables.items()):
            return tuple(self.AllTables.items())
        TBLS = self.CURS.execute("SELECT * FROM all_tables").fetchall()
        for i in TBLS:
            command = f"PRAGMA table_info({i[0]})"
            LST = []
            for j in self.CURS.execute(command).fetchall():
                LST.append(j[1])
            self.AllTables[i[0]] = LST
        return tuple(self.AllTables.items())

    def execute(self, command, returns=True):
        if returns:
            return self.CURS.execute(command).fetchall()
        else:
            self.CURS.execute(command)
        self.CONN.commit()

    def ResetDB(self):

        L = self.CURS.execute("SELECT table_name FROM all_tables")
        for i in L:
            command = f"DROP TABLE [{i[0]}]"
            self.CURS.execute(command)
        command = f"DELETE FROM all_tables"
        self.CURS.execute(command)

    def closeConn(self):
        self.CONN.commit()
        self.CONN.close()
