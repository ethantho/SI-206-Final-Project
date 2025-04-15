import sqlite3

import game_data
import movie_data
import stocks_data

if __name__ == "__main__":
    conn = sqlite3.connect("db.sqlite3")

    game_data.main(conn)
    movie_data.main(conn)
    stocks_data.main(conn)