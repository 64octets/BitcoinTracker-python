# Author: Abid H. Mujtaba
# Date: 2014-03-31
#
# Module containing methods that are required by a number of other scripts/modules.

import datetime
import rpy2.robjects as robjects
import math
import os
import time


def get_db():
    """
    Gives the absolute path to the sqlite3 database used by the application.
    """

    dirname = os.path.dirname(os.path.realpath(__file__))

    return os.path.join(dirname, 'data.db')


def chop_btc(btc):
    """
    Method for chopping the BTC amount so that it has the standard 8 decimal precision.
    """

    return math.floor(btc * 1e8) / 1e8


def max_price(prices):
    """
    Function that uses R to find the maximum price from a list of float prices.
    """

    return robjects.r['max'](prices)[0]        # We use the R object to access the 'max' function, pass in the list of prices and then get the 1st element to get the result


def format_time(t):
    """
    Method for converting a unix epoch timestamp to human-readable format.
    """

    return datetime.datetime.fromtimestamp(t).strftime("%m-%d %H:%M")


def current_time():
    """
    Method for getting the current time in a human-readable format.
    """

    return datetime.datetime.fromtimestamp(time.time()).strftime("%m-%d %H:%M")