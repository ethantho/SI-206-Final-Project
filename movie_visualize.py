import sqlite3
import csv
import colorsys
import random

import matplotlib.pyplot as plt

def get_index(array: list[tuple], index: int):
    return list(map(lambda x: x[index], array))

def gen_array(values):
    arr = [0 for _ in range(26)]
    for entry in values:
        arr[entry[0] - 2000] += entry[2]
    return arr

def add_arrays(l1, l2):
    for i, x in enumerate(l2):
        l1[i] += x
    pass

def main(conn: sqlite3.Connection):
    releases_by_year = {}
    values_overall = conn.execute(
        "SELECT CAST(release_date AS INT) AS year, COUNT(*) FROM Movies GROUP BY year;"
    ).fetchall()
    
    values_genre = conn.execute(
        "SELECT CAST(release_date AS INT) AS year, MovieGenres.genre_name, COUNT(*) "
        "FROM Movies " 
        "JOIN MovieGenres ON genre_id = MovieGenres.id "
        "WHERE year BETWEEN 2000 AND 2025 "
        "GROUP BY year, genre_id "
    ).fetchall()
    #print(values_genre)
    all_genres = conn.execute(
        "SELECT genre_name FROM MovieGenres"
    ).fetchall()

    plt.cla()
    values = [0 for _ in range(26)]
    for i, genre in enumerate(get_index(all_genres, 0)):
        # print(genre)
        genre_filtered = list(filter(lambda x: x[1] == genre, values_genre))
        genre_values = gen_array(genre_filtered)
        # print(genre_values)
        color = colorsys.hsv_to_rgb(i * 1/len(all_genres), 1, 1)
        plt.bar(
            [i for i in range(2000, 2026)],
            genre_values,
            bottom=values,
            color=color,
            label=genre
        )
        add_arrays(values, genre_values)
        # print(values)
    plt.xlabel("Year")
    plt.ylabel("# Movies Released")
    plt.title("# Movies Released Per Year (By Genre)")
    plt.legend(markerscale=0.5)
    
    with open("movie_calculations_with_genre.csv", "w") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(["year", "genre", "count"])
        writer.writerows(values_genre)
    plt.savefig("movies_by_genre.png", bbox_inches='tight')
    #plt.show()
    
    plt.cla()
    with open("movie_calculations.csv", "w") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(["year", "count"])
        writer.writerows(values_overall)

    plt.bar(get_index(values_overall, 0), get_index(values_overall, 1))
    plt.xlabel("Year")
    plt.ylabel("# Of Movies Released")
    plt.title("Movies released per year")
    plt.savefig("movie.png", bbox_inches='tight')
    #plt.show()
    return

    


if __name__ == "__main__":
    conn = sqlite3.connect("db.sqlite3")
    main(conn)