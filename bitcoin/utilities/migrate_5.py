#! /usr/bin/python
#
#
# Copyright 2014 Abid Hasan Mujtaba
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Author: Abid H. Mujtaba
# Date: 2014-04-17
#
# This script reads buy and price data from the database, calculates the sma and lma (Short and Long moving averages)
# and stores them in the database.


import sqlite3

from bitcoin import get_db, round2
from bitcoin.utilities.moving_averages import moving_average


if __name__ == '__main__':

    conn = sqlite3.connect( get_db() )
    cursor = conn.cursor()

    s_time = []
    s_buy = []
    s_sell = []

    print("Reading in time and prices from database.")

    for values in cursor.execute('''SELECT "time", "buy", "sell" FROM "prices"'''):

        s_time.append( values[0] )
        s_buy.append( values[1] )
        s_sell.append( values[2] )

    print("Calculating the Short and Long Moving Averages")

    b_sma = moving_average(s_buy, 10)
    b_lma = moving_average(s_buy, 25)

    s_sma = moving_average(s_sell, 10)
    s_lma = moving_average(s_sell, 25)


    print("Writing sma and lma to database.")

    for ii in range(len(s_buy)):

        t = s_time[ii]
        bsma = b_sma[ii]
        blma = b_lma[ii]
        ssma = s_sma[ii]
        slma = s_lma[ii]

        bdelta = round2(bsma - blma)            # Calculate the delta value (how separated the short and long moving averages are at any given time)
        sdelta = round2(ssma - slma)

        cursor.execute('''REPLACE INTO "averages" ("time", "b_sma", "b_lma", "b_delta", "s_sma", "s_lma", "s_delta") VALUES (?,?,?,?,?, ?, ?)''', (t, bsma, blma, bdelta, ssma, slma, sdelta,))

    conn.commit()       # Commit changes
    conn.close()        # Close connection

    print("Done")