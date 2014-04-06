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
# Date: 2014-04-05
#
# This script reads buy and price data from the database, calculates the first and second finite differences and stores
# it in the database.


import rpy2.robjects as robjects
import sqlite3

from bitcoin import get_db, round2


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


    # We now use R to calculate the differences:
    diff = robjects.r['diff']                       # Access 'diff' method from R

    cbuy = robjects.FloatVector(s_buy)              # Convert list to R vector
    csell = robjects.FloatVector(s_sell)

    d1buy = diff(cbuy, differences=1)               # Calculate 1st finite difference
    d1sell = diff(csell, differences=1)

    d2buy = diff(cbuy, differences=2)               # Calculate 2nd finite difference
    d2sell = diff(csell, differences=2)


    print("Writing differences to database.")

    for ii in range(len(d2buy)):

        t = s_time[ii+2]
        d1_buy = round2( d1buy[ii+1] )
        d1_sell = round2( d1sell[ii+1] )
        d2_buy = round2( d2buy[ii] )
        d2_sell = round2( d2sell[ii] )

        cursor.execute('''REPLACE INTO "diffs" ("time", "d1_buy", "d1_sell", "d2_buy", "d2_sell") VALUES (?,?,?,?,?)''', (t, d1_buy, d1_sell, d2_buy, d2_sell,))


    conn.commit()       # Commit changes
    conn.close()        # Close connection

    print("Done")