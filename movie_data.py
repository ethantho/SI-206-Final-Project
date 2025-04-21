import json
import random
import string
import requests
import sqlite3
import time
import datetime as dt
import functools
import warnings

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
            "genre_name TEXT UNIQUE"
        ")"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS Movies (" \
            "id INTEGER PRIMARY KEY AUTOINCREMENT, " \
            "imdb_id TEXT NOT NULL UNIQUE, " \
            "name TEXT, " \
            "release_date DATETIME NOT NULL, " \
            #"box_office INTEGER, " \
            "genre_id INTEGER, " \
            "FOREIGN KEY(genre_id) REFERENCES MovieGenres(id) "
        ")"
    )

    conn.commit()

def get_random_movie_info(conn: sqlite3.Connection, cycles=3):
    count = conn.execute("SELECT COUNT(*) FROM ImdbInfo WHERE checked = 0").fetchone()[0]
    print (count)
    if count > 25:
        return

    for _ in range(cycles):
        rand_name = "".join(random.choices(string.ascii_lowercase, k=3))
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
        else:
            print("Error fetching imdb info")
    conn.commit()

@functools.cache
def get_genre(genre: str, conn: sqlite3.Connection) -> int:
    val = conn.execute("SELECT id FROM MovieGenres WHERE genre_name = ?", (genre, )).fetchone()

    if val is None:
        conn.execute("INSERT INTO MovieGenres(genre_name) VALUES (?)", (genre, ))
        return conn.execute("SELECT id FROM MovieGenres WHERE genre_name = ?", (genre, )).fetchone()[0]
    else:
        return val[0]

def parse_movie_obj(imdb_id: str, data: dict, conn: sqlite3.Connection):
    name = data.get("Title")
    try:
        release_timestamp = dt.datetime.strptime(data.get("Released", ""), "%d %b %Y")
    except ValueError:
        return

    genre_id = get_genre(data.get("Genre", "").split(",")[0], conn)
    warnings.simplefilter("ignore", DeprecationWarning)
    conn.execute(
        "INSERT OR IGNORE INTO Movies " \
        "(imdb_id, name, release_date, genre_id) " \
        "VALUES (?, ?, ?, ?)",
        (imdb_id, name, release_timestamp, genre_id)
    )

def fetch_omdb_info(conn: sqlite3.Connection):
    movies = conn.execute(
        "SELECT id FROM ImdbInfo WHERE checked = 0 LIMIT 25"
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
            #print("Not a movie")
            continue
        parse_movie_obj(imdb_id, response, conn)
    conn.executemany("UPDATE ImdbInfo SET checked=1 WHERE id=?", movies)
    conn.commit()

def main(conn: sqlite3.Connection):
    initialize_tables(conn)
    get_random_movie_info(conn, 3)
    fetch_omdb_info(conn)
    # with open("sample-movie.json") as file:
    #     parse_movie_obj("tt27829165", json.load(file), conn)
    #     conn.commit()
        

if __name__ == "__main__":
    conn = sqlite3.connect("db.sqlite3")
    main(conn)