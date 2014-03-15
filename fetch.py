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
import json
import sqlite3
import sys
import time
import urllib2


TICKER_URL = "https://www.bitstamp.net/api/ticker/"


if __name__ == '__main__':

    data = json.load(urllib2.urlopen(TICKER_URL))

    buy = data["ask"]
    sell = data["bid"]

    now = int(time.time())        # Get current unix time


    if len(sys.argv) > 1 and sys.argv[1] == '--insert':         # The --insert switch has been passed so we insert the data in to the sqlite3 database

        conn = sqlite3.connect('/home/abid/scripts/python/bitcoin/data.db')
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO "prices" ("time", "buy", "sell") VALUES (?, ?, ?)''', (now, buy, sell))

        conn.commit()
        conn.close()

    else:           # The --insert switch has NOT been passed so we print the fetched data to stdout

        timestring = datetime.fromtimestamp(now).strftime("%H:%M:%S")

        print("{} : {} - {}".format(timestring, buy, sell))