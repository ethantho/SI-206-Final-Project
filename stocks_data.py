# Ethan Leach (lethan), Ethan Thompson (ethantho), Saicharan Vemuri (scharan)
# SI 206 - Final Project
# Stock Market data collection (taking from DJI ETF)

import json
import datetime
from dateutil import parser
import requests
import sqlite3


def main(conn: sqlite3.Connection):

    url = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=DIA&apikey=PH5DHJILCNX7HL81"

    cur = conn.cursor()

    first_pass = True

    cur.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'stocks'")
    stocks_exists = cur.fetchone()
    if stocks_exists:
        first_pass = False
    else:
        first_pass = True

    cur.execute("CREATE TABLE IF NOT EXISTS stocks (date DATETIME PRIMARY KEY, open FLOAT, high FLOAT, low FLOAT, close FLOAT)")

    data = requests.get(url).json()

    stock_data = data["Monthly Time Series"]

    item_counter = 0

    if first_pass:
        for item in stock_data:
            if item_counter > 20:
                break

            dt_date = parser.parse(item)

            cur.execute("INSERT INTO stocks VALUES (?,?,?,?,?)", (dt_date, float(stock_data[item]["1. open"]), float(stock_data[item]["2. high"]), float(stock_data[item]["3. low"]), float(stock_data[item]["4. close"])))

            item_counter += 1
    else:
        cur.execute("SELECT date FROM stocks ORDER BY date ASC LIMIT 1")
        most_recent_entry = cur.fetchone()[0]

        for item in stock_data:

            if item_counter >= 20:
                break

            dt_date = parser.parse(item)

            dt_mre = parser.parse(most_recent_entry)

            if (dt_date >= dt_mre):
                continue

            cur.execute("INSERT INTO stocks VALUES (?,?,?,?,?)", (dt_date, stock_data[item]["1. open"], stock_data[item]["2. high"], stock_data[item]["3. low"], stock_data[item]["4. close"]))

            item_counter += 1

    conn.commit()

    return


if __name__ == "__main__":
    conn = sqlite3.connect("db.sqlite3")
    main(conn)
