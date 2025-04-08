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

    STOCKS = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=DOW&apikey=PH5DHJILCNX7HL81"
    GAMES = ""
    MOVIES = ""

def get_api_data(source):
    """
    Gets data from the given source in the form of a dictionary

    Parameters:
        source (Source enum class) - the source to collect data from
    """

    if source == Source.STOCKS.name:
        return requests.get(Source.STOCKS.value).json()
    elif source == Source.GAMES.name:
        return requests.get(Source.GAMES.value).json()
    elif source == Source.MOVIES.name:
        return requests.get(Source.MOVIES.value).json()
    
    return