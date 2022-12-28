import sqlite3 as sq
from sqlite3 import Error

projects_database = r'/home/petr/Dokumenty/pyladies/Laber_maker_02/db/projects_database.db'
cell_culture_database = r"/home/petr/Dokumenty/pyladies/Laber_maker_02/db/CC_database.db"
bac_database = r'/home/petr/Dokumenty/pyladies/Laber_maker_02/db/bac_database.db'
phage_database = r'/home/petr/Dokumenty/pyladies/Laber_maker_02/db/phage_database.db'
dev_database = r'/home/petr/Dokumenty/pyladies/Laber_maker_02/db/dev_database.db'


def project_database_con():
    data = []
    try:
        conn = sq.connect(projects_database)  # vytvoří spojení s databází
        print("spojeno", sq.version)
        cur = conn.cursor()  # umožní zapisování/čtení do dazabáze
        cur.execute("""CREATE TABLE IF NOT EXISTS projects(
                            no int PRIMARY KEY,
                            name text,
                            finished text);""")  # vytvoření tabulky, pokud už není
        conn.commit()
        print("tabulka vytvořena")
        cur.execute("SELECT * FROM projects")
        rows = cur.fetchall()
        for row in rows:
            data.append(row)
    except Error as e:
        print(e)
    data.sort()
    print("projekty", data)
    return data


def add_project(item):
    entries = []
    try:
        conn = sq.connect(projects_database)  # vytvoří spojení s databází
        print("spojeno", sq.version)
        cur = conn.cursor()  # umožní zapisování do dazabáze
        cur.execute("""CREATE TABLE IF NOT EXISTS projects(
                                no int PRIMARY KEY,
                                name text,
                                finished text);""")  # vytvoření tabulky
        conn.commit()
        entries.clear()
        entries.append(item)
        print(entries)
        cur.executemany("INSERT INTO projects VALUES(?, ?, ?)", entries)
        conn.commit()
        print("hotovo")
    except Error as e:
        print(e)
    print(entries)
    return entries


def delete_project(no):
    try:
        conn = sq.connect(projects_database)  # vytvoří spojení s databází
        print("spojeno", sq.version)
        cur = conn.cursor()  # umožní zapisování do dazabáze
        sql = "DELETE FROM projects WHERE no = " + str(no)
        cur.execute(sql)
        conn.commit()
        print("smazáno", no)
    except Error as e:
        print(e)


def cell_culture_database_con():
    data = []
    try:
        conn = sq.connect(cell_culture_database)  # vytvoří spojení s databází
        print("spojeno", sq.version)
        cur = conn.cursor()  # umožní zapisování do dazabáze
        cur.execute("""CREATE TABLE IF NOT EXISTS cell_line (
                                name int PRIMARY KEY,
                                medium text);""")  # vytvoření tabulky
        conn.commit()
        print("tabulka vytvořena")
        cur.execute("SELECT * FROM projects")
        rows = cur.fetchall()
        for row in rows:
            data.append(row)
            print(row)
    except Error as e:
        print(e)
    data.sort()
    print("buněčné linie", data)
    return data


def bac_database_con():
    data = []
    try:
        conn = sq.connect(bac_database)  # vytvoří spojení s databází
        print("spojeno", sq.version)
        cur = conn.cursor()  # umožní zapisování do dazabáze
        cur.execute("""CREATE TABLE IF NOT EXISTS bacteria (
                                    name int PRIMARY KEY,
                                    medium text);""")  # vytvoření tabulky
        conn.commit()
        print("tabulka vytvořena")
        cur.execute("SELECT * FROM projects")
        rows = cur.fetchall()
        for row in rows:
            data.append(row)
            print(row)
    except Error as e:
        print(e)
    data.sort()
    print("bakterie", data)
    return data


def phage_database_con():
    pass


def dev_database_con():
    pass
