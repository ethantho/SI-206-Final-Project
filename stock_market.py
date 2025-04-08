# Ethan Leach (lethan), Ethan Thompson (ethantho), Saicharan Vemuri (scharan)
# SI 206 - Final Project
# Stock Market script

import main

def get_data():
    """
    Get data from API call as a dictionary
    """
    return main.get_api_data(main.Source.STOCKS)

