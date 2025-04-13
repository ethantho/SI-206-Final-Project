import sqlite3
import matplotlib.pyplot as plot

def year_to_timestamp(year):
    return (year - 1970) * 365 * 24 * 60 * 60

def main(conn: sqlite3.Connection):
    cur = conn.cursor()
    names = cur.execute("SELECT name FROM games").fetchall()
    release_dates = cur.execute("SELECT release_date FROM games").fetchall()

    releases_by_year = {}
    for i in range(1970, 2024):
        releases_by_year[i] = int(cur.execute("SELECT COUNT(*) FROM games WHERE release_date > ? AND release_date < ?", (year_to_timestamp(i), year_to_timestamp(i+1))).fetchone()[0])

    plot.bar(releases_by_year.keys(), releases_by_year.values())
    plot.xlabel('Year')
    plot.ylabel('Number of Games Released')
    plot.show()


if __name__ == "__main__":
    conn = sqlite3.connect("db.sqlite3")
    main(conn)

