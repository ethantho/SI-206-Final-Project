import sqlite3
import matplotlib.pyplot as plot
from dateutil import parser

def main(conn: sqlite3.Connection):
    cur = conn.cursor()

    avg_price_by_month = {}

    raw_data = cur.execute("SELECT date, high, low FROM stocks").fetchall()

    for item in raw_data:
        avgprice = (item[1] + item[2]) / 2.0
        avg_price_by_month[item[0]] = avgprice
    
    plot.cla()
    plot.plot(avg_price_by_month.keys(), avg_price_by_month.values())
    plot.xlabel('Month')
    plot.title("Average DIA Stock Price By Month")
    plot.ylabel('Average DIA Stock Price (USD)')
    
    plot.savefig("stocks.png")
    #plot.show()


    with open("stock_calculations.txt", 'w') as file:
        file.write("Average stock prices per month in our sample:\n")
        for month, price in avg_price_by_month.items():
            file.write(f"{month}: ${price}\n")


if __name__ == "__main__":
    conn = sqlite3.connect("db.sqlite3")
    main(conn)