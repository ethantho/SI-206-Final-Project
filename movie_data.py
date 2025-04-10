import json
import random
import string
import requests
import sqlite3

IMDB_QUERY_URL = "https://imdb.iamidiotareyoutoo.com/search"
OMDB_QUERY_URL = "http://www.omdbapi.com/?apikey=94921550&"

def initialize_tables(conn: sqlite3.Connection):
    conn.execute(
        "CREATE TABLE IF NOT EXISTS ImdbInfo (" \
            "id TEXT UNIQUE PRIMARY KEY NOT NULL, " \
            "checked BOOLEAN NOT NULL DEFAULT 0" \
        ")"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS MovieGenres (" \
            "id INTEGER PRIMARY KEY AUTOINCREMENT, " \
            "genre_name TEXT"
        ")"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS Movies (" \
            "id INTEGER PRIMARY KEY AUTOINCREMENT, " \
            "ibdb_id TEXT NOT NULL, " \
            "name TEXT, " \
            "release_date INTEGER, " \
            "box_office INTEGER, " \
            "genre_id INTEGER, " \
            "FOREIGN KEY(genre_id) REFERENCES MovieGenres(id) "
        ")"
    )

    conn.commit()

def get_random_movie_info(cur: sqlite3.Cursor, conn: sqlite3.Connection, cycles=3):
    for _ in range(cycles):
        rand_name = "".join(random.choices(string.ascii_lowercase, k=5))
        query = f'{IMDB_QUERY_URL}?q="{rand_name}"'

        req = requests.get(query)
        
        if not req.ok:
            return
        body = json.loads(req.text) 
        if body["error_code"] == 200:
            conn.executemany(
                "INSERT OR IGNORE INTO ImdbInfo (id) VALUES (?)", 
                map(lambda x: (x["#IMDB_ID"],), body["description"])
            )
    conn.commit()

def fetch_omdb_info(conn: sqlite3.Connection):
    movies = conn.execute(
        "SELECT id FROM ImdbInfo WHERE checked = 0 LIMIT 3"
    ).fetchall()

    for imdb_id in map(lambda x: x[0], movies):
        query = OMDB_QUERY_URL + f"i={imdb_id}"
        req = requests.get(query)

        if not req.ok:
            continue
        response = json.loads(req.text)
        if response["Response"] == "False":
            continue

        if response["Type"] != "movie":
            print("Not a movie")
            continue
        print(response)
    
    #conn.executemany("UPDATE ImdbInfo SET checked=1 WHERE id=?", movies)

def main(conn: sqlite3.Connection):
    cur = conn.cursor()    
    initialize_tables(conn)
    #get_random_movie_info(cur, conn, 5)
    fetch_omdb_info(conn)

if __name__ == "__main__":
    conn = sqlite3.connect("db.sqlite3")
    main(conn)