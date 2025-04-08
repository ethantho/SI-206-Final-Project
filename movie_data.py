import json
import random
import string
import requests
import sqlite3

IMDB_QUERY_URL = "https://imdb.iamidiotareyoutoo.com/search"

def get_random_movie_info(cur: sqlite3.Cursor, conn: sqlite3.Connection, cycles=3):
    rand_name = "".join(random.choices(string.ascii_lowercase, k=5))
    query = f'{IMDB_QUERY_URL}?q="{rand_name}"'

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

if __name__ == "__main__":
    conn = sqlite3.connect("db.sqlite3")
    main(conn)