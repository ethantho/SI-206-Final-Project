import sqlite3
import csv

import matplotlib.pyplot as plt

def get_index(array: list[tuple], index: int):
    return list(map(lambda x: x[index], array))

def main(conn: sqlite3.Connection):
    releases_by_year = {}
    values = conn.execute(
        "SELECT CAST(release_date AS INT) AS year, COUNT(*) FROM Movies GROUP BY year;"
    ).fetchall()
    
    values_genre = conn.execute(
        "SELECT CAST(release_date AS INT) AS year, MovieGenres.genre_name, COUNT(*) "
        "FROM Movies " 
        "JOIN MovieGenres ON genre_id = MovieGenres.id "
        "GROUP BY year, genre_id "
    ).fetchall()
    
    with open("movie_calculations.csv", "w") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(["year", "count"])
        writer.writerows(values)

    plt.bar(get_index(values, 0), get_index(values, 1))
    plt.xlabel("Year")
    plt.ylabel("# Of Movies Released")
    plt.show()


if __name__ == "__main__":
    conn = sqlite3.connect("db.sqlite3")
    main(conn)