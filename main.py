# Ethan Leach (lethan), Ethan Thompson (ethantho), Saicharan Vemuri (scharan)
# SI 206 - Final Project
# Main script

import requests
import sqlite3
from enum import Enum

class Source(Enum):
    """
    Source enum class
    Stores the API link of each source in a name
    """

    # Stock market API returns the last 100 days of data from Dow Jones (DOW)
    STOCKS = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=DIA&outputsize=full&apikey=PH5DHJILCNX7HL81"
    GAMES = ""
    MOVIES = ""

def get_api_data(source):
    """
    Gets data from the given source in the form of a dictionary

    Parameters:
        source (Source enum class) - the source to collect data from
    """

    if source == Source.STOCKS:
        return requests.get(Source.STOCKS.value).json()
    elif source == Source.GAMES:
        return requests.get(Source.GAMES.value).json()
    elif source == Source.MOVIES:
        return requests.get(Source.MOVIES.value).json()
    
    return
