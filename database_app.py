import sqlite3 as sq
from sqlite3 import Error

database = r"/home/petr/Dokumenty/pyladies/ucimese_SQLITE/db/labelmaker02database.db"
entries =[]
def add_project_to_database():
    try:
        conn = sq.connect(database)  # vytvoří spojení s databází
        print("spojeno", sq.version)
        cur = conn.cursor()  # umožní zapisování do dazabáze
        cur.execute("""CREATE TABLE IF NOT EXISTS projects(
                                no text,
                                name text,
                                finished text);""")  # vytvoření tabulky
        conn.commit()
        print("tabulka vytvořena")
        user_input()
        cur.executemany("INSERT INTO projects VALUES(?, ?, ?)", entries)
        conn.commit()
        print("hotovo")
    except Error as e:
        print(e)

        return entries