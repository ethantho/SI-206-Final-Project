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

    price_each_jan = {}
    for month, price in avg_price_by_month.items():
        year = month[0:4]
        month = month[5:7]
        if month == '01':
            price_each_jan[year] = price
    price_each_jan = dict(reversed(list(price_each_jan.items())))

    
    plot.cla()
    #plot.plot(avg_price_by_month.keys(), avg_price_by_month.values())
    plot.plot(price_each_jan.keys(), price_each_jan.values())
    plot.xlabel('Year')
    plot.xticks(rotation=45, ha='right')
    plot.title("Average DIA Stock Price By Year")
    plot.ylabel('Average DIA Stock Price (USD)')
    
    plot.savefig("stocks.png")
    #plot.show()


    with open("stock_calculations.txt", 'w') as file:
        file.write("Average stock prices per Month in our sample:\n")
        for month, price in avg_price_by_month.items():
            file.write(f"{month}: ${price}\n")


if __name__ == "__main__":
    conn = sqlite3.connect("db.sqlite3")
    main(conn)