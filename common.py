# Author: Abid H. Mujtaba
# Date: 2014-03-31
#
# Module containing methods that are required by a number of other scripts/modules.

import math
import os

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
