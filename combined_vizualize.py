import sqlite3
import csv
import matplotlib.pyplot as plt

from movie_visualize import get_index



def main(conn: sqlite3.Connection):
    values = conn.execute(
    """
        WITH RECURSIVE generate_series(value) AS (
            SELECT 2000
            UNION ALL
            SELECT value + 1 FROM generate_series
            WHERE value + 1 <= 2024
        )
        SELECT 
            value,
            (SELECT COUNT(*) FROM Movies WHERE CAST(release_date AS INT) = value) as movie_count,
            (SELECT COUNT(*) FROM Games WHERE (release_date / 365 / 24 / 60 / 60 + 1970) = value) as game_count, 
    		(SELECT AVG(close) FROM Stocks WHERE CAST(date AS INT) = value) as stocks
        FROM generate_series
    """
    ).fetchall()
    years = get_index(values, 0)
    movies = get_index(values, 1)
    games = get_index(values, 2)
    stocks = get_index(values, 3)

    with open("combined.csv", "w") as file:
        csv_file = csv.writer(file, lineterminator="\n")
        csv_file.writerow(["year", "movie_count", "game_count", "avg_stock_close"])
        csv_file.writerows(values)

    width=0.45
    fig = plt.figure()
    ax = fig.add_subplot(111)

    stock_scaling_factor = 20

    rect1 = ax.bar(list(map(lambda x: x-width/2, years)), movies, width)
    rect2 = ax.bar(list(map(lambda x: x+width/2, years)), games, width)
    line1 = ax.plot(years, list(map(lambda x: x/stock_scaling_factor, stocks)), "r-")

    ax.legend((rect1[0], rect2[0], line1[0]), ("Movies", "Games", "Avg Stock Price"))
    plt.title("Stock Prices vs Movies & Game Releases Per Year (2000-2025)")
    plt.savefig("combined.png", bbox_inches='tight')
    #plt.show()



if __name__ == "__main__":
    conn = sqlite3.connect("db.sqlite3")
    main(conn)