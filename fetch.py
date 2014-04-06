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
# Date: 2014-02-25
#
# This script fetches data from the BitStamp backedn API and prints it to stdout

from datetime import datetime
import sqlite3
import sys
import time

import bitcoin
from bitcoin import client, round2
from bitcoin.utilities.weighted_average import single_weighted_average, NUM_WEIGHING_SAMPLES, WEIGHING_FUNCTION


if __name__ == '__main__':

    data = client.current_price()

    buy = data["buy"]
    sell = data["sell"]

    now = int(time.time())        # Get current unix time


    if len(sys.argv) > 1 and sys.argv[1] == '--insert':         # The --insert switch has been passed so we insert the data in to the sqlite3 database

        conn = sqlite3.connect( bitcoin.get_db() )
        cursor = conn.cursor()

        # We pull previous (NUM_WEIGHING_SAMPLES - 1) prices to calculate the current weighted_average of the prices:
        
        s_buy = []
        s_sell = []

        for values in cursor.execute('''SELECT "buy", "sell" FROM "prices" ORDER BY "time" DESC LIMIT ?''', (NUM_WEIGHING_SAMPLES - 1,)):

            s_buy.append( values[0] )
            s_sell.append( values[1] )

        # Append the current values
        s_buy.append( float(buy) )
        s_sell.append( float(sell) )

        wbuy = single_weighted_average(s_buy, NUM_WEIGHING_SAMPLES, WEIGHING_FUNCTION)
        wsell = single_weighted_average(s_sell, NUM_WEIGHING_SAMPLES, WEIGHING_FUNCTION)


        # We JOIN the "prices" and "diffs" table NATURALly (which means on the common columns, in this case only "time") and then extract the latest value of the prices and 1st finite
        # difference. We will use these to calculate the current 1st and 2nd finite differences.
        values = cursor.execute('''SELECT "buy", "sell", "d1_buy", "d1_sell" FROM "prices" NATURAL JOIN "diffs" ORDER BY "time" DESC LIMIT 1''').fetchone()

        last_buy = values[0]
        last_sell = values[1]
        last_d1_buy = values[2]
        last_d1_sell = values[3]

        d1_buy = round2( float(buy) - last_buy )             # Calculate the finite differences and round to 2 decimal places
        d1_sell = round2( float(sell) - last_sell )

        d2_buy = round2( d1_buy - last_d1_buy )
        d2_sell = round2( d1_sell - last_d1_sell )


        cursor.execute('''INSERT INTO "prices" ("time", "buy", "sell", "wa_buy", "wa_sell") VALUES (?, ?, ?, ?, ?)''', (now, buy, sell, wbuy, wsell))

        cursor.execute('''INSERT INTO "diffs" ("time", "d1_buy", "d1_sell", "d2_buy", "d2_sell") VALUES (?, ?, ?, ?, ?)''', (now, d1_buy, d1_sell, d2_buy, d2_sell))

        conn.commit()
        conn.close()

    else:           # The --insert switch has NOT been passed so we print the fetched data to stdout

        timestring = datetime.fromtimestamp(now).strftime("%H:%M:%S")

        print("{} : {} - {}".format(timestring, buy, sell))
