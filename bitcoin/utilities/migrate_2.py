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
# Date: 2014-03-20
#
# This script reads buy and price data from the database, calculates the weighted average and stores it in the database.


import sqlite3

from bitcoin.utilities.weighted_average import weighted_running_average, NUM_WEIGHING_SAMPLES, WEIGHING_FUNCTION


if __name__ == '__main__':

    conn = sqlite3.connect('../data.db')
    cursor = conn.cursor()

    s_time = []
    s_buy = []
    s_sell = []

    for values in cursor.execute('''SELECT "time", "buy", "sell" FROM "prices"'''):

        s_time.append( values[0] )
        s_buy.append( values[1] )
        s_sell.append( values[2] )

    print("Number of records to be processed: " + str(len(s_time)))

    wa_buy = weighted_running_average( s_buy, NUM_WEIGHING_SAMPLES, WEIGHING_FUNCTION )
    wa_sell = weighted_running_average( s_sell, NUM_WEIGHING_SAMPLES, WEIGHING_FUNCTION )

    print("Weighted Running Averages calculated.\nInserting in to database...")


    for ii in range(len(s_time)):

        time = s_time[ii]
        wbuy = wa_buy[ii]
        wsell = wa_sell[ii]

        cursor.execute('''UPDATE "prices" SET "wa_buy" = ?, "wa_sell" = ? WHERE "time" = ?''', (wbuy, wsell, time))

    conn.commit()       # Commit changes
    conn.close()        # Close connection

    print("Done")
