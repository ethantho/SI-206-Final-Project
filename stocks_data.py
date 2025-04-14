# Ethan Leach (lethan), Ethan Thompson (ethantho), Saicharan Vemuri (scharan)
# SI 206 - Final Project
# Stock Market script

import json
import datetime
from dateutil import parser
import requests
import sqlite3


def main(conn: sqlite3.Connection):

    url = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=DIA&apikey=PH5DHJILCNX7HL81"

    cur = conn.cursor()

    first_pass = True

    cur.execute("IF EXISTS TABLE WHERE TABLE_NAME = 'stocks' SELECT 1 ELSE SELECT 0")
    if cur.fetchone()[0] == 0:
        first_pass = True
    else:
        first_pass = False

    cur.execute("CREATE TABLE IF NOT EXISTS stocks (id INTEGER PRIMARY KEY, date DATETIME, open FLOAT, high FLOAT NOT, low FLOAT, close FLOAT)")

    data = requests.get(url).json()

    stock_data = data["Monthly Time Series"]

    item_counter = 0

    if first_pass:
        for item in stock_data:
            if item_counter > 20:
                break

            dt_date = parser.parse(item)

            cur.execute("INSERT INTO stocks VALUES (?,?,?,?,?)", (dt_date, stock_data[item]["1. open"], stock_data[item]["2. high"], stock_data[item]["3. low"], stock_data[item]["4. close"]))

            item_counter += 1
    else:
        cur.execute("SELECT date FROM stocks ORDER BY id DESC LIMIT 1")
        most_recent_entry = cur.fetchone()[0]

        for item in stock_data:

            if item_counter > 20:
                break
            
            dt_item = parser.parse(item)

            if (dt_item >= most_recent_entry):
                continue

            cur.execute("INSERT INTO stocks VALUES (?,?,?,?,?)", (dt_date, stock_data[item]["1. open"], stock_data[item]["2. high"], stock_data[item]["3. low"], stock_data[item]["4. close"]))

            item_counter += 1


    return


if __name__ == "__main__":
    conn = sqlite3.connect("db.sqlite3")
    main(conn)
