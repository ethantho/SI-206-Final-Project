import sqlite3

import game_visualizations
import movie_visualize
import stocks_visualize
import combined_vizualize

if __name__ == "__main__":
    conn = sqlite3.connect("db.sqlite3")
    game_visualizations.main(conn)
    movie_visualize.main(conn)
    stocks_visualize.main(conn)
    combined_vizualize.main(conn)