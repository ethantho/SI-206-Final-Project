import json
import random
import string
import requests
import sqlite3

IMDB_QUERY_URL = "https://imdb.iamidiotareyoutoo.com/search"

def get_random_movie_info(cur: sqlite3.Cursor, conn: sqlite3.Connection, cycles=3):
    rand_name = "".join(random.choices(string.ascii_lowercase, k=5))
    query = f'{IMDB_QUERY_URL}?q="{rand_name}"'

    req = requests.get(query)
    
    if not req.ok:
        return
    body = json.loads(req.text) 
    if body["error_code"] == 200:
        #print(body)
        conn.executemany(
            "INSERT INTO ImdbInfo (id) VALUES (?)", 
            map(lambda x: (int(x["#IMDB_ID"].strip("t")),), body["description"])
        )
    conn.commit()

def initialize_tables(conn: sqlite3.Connection):
    conn.execute(
        "CREATE TABLE IF NOT EXISTS ImdbInfo (" \
            "id INTEGER UNIQUE PRIMARY KEY NOT NULL, " \
            "checked BOOLEAN NOT NULL DEFAULT 0" \
        ")"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS Movies (" \
            "id INTEGER PRIMARY KEY AUTOINCREMENT, " \
            "ibdb_id INTEGER NOT NULL, " \
            "name TEXT, " \
            "release_date INTEGER, " \
            "box_office INTEGER, " \
            "FOREIGN KEY(ibdb_id) REFERENCES ImdbInfo(id)"
        ")"
    )
    conn.commit()

def main(conn: sqlite3.Connection):
    cur = conn.cursor()    
    initialize_tables(conn)
    get_random_movie_info(cur, conn, 3)

if __name__ == "__main__":
    conn = sqlite3.connect("db.sqlite3")
    main(conn)