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
# Date: 2014-03-29
#
# Get transactions from after the specified date (inclusive) from the BitStamp API and stores the relevant
# information in a CSV file for inclusion in our spreadsheet.


from dateutil.parser import parse
import pytz
import sys

import common
common.add_parent_to_path()

import bitcoin.client


if __name__ == '__main__':

    threshold = sys.argv[1]     # Date containing the threshold date after which to store transactions in the csv file
    dt = pytz.utc.localize( parse(threshold) )      # Convert sys arg to datetime


    print("Fetching transactions from BitStamp server ...")
    data = bitcoin.client.transactions()

    fout = open("transactions.csv", 'w')
    sold = []       # List of "sell" transactions
    bought = []     # List of "buy" transactions

    print("Inserting data in to CSV file ...")

    for trx in data:

        dts = pytz.utc.localize( parse( trx['datetime'] ))      # Convert transaction time-string to datetime object

        if trx['type'] == 2 and dts > dt:

            usd = float(trx['usd'])
            btc = float(trx['btc'])
            rate = float(trx['btc_usd'])
            fee = float(trx['fee'])

            date = dts.strftime('%m/%d')
            time = dts.strftime('%H:%M')

            if usd > 0:      # BTC Sold

                output = "BS, {date}, {time}, {rate}, {btc}, {usd}\n".format(date=date, time=time, rate=rate, btc=-btc, usd=usd - fee)     # Note we incorporate the fee in the cost
                sold.append(output)

            else:           # BTC Bought

                output = "BS, {date}, {time}, {rate}, {btc}, {usd}\n".format(date=date, time=time, rate=rate, btc=btc, usd=-usd + fee)
                bought.append(output)


    bought.reverse()        # Reverse order of lists to get chronological order
    sold.reverse()

    fout.write("Buy:\n\n")
    for line in bought: fout.write(line)
    fout.write("\nSell:\n\n")
    for line in sold: fout.write(line)

    fout.close()

    print("Done")
