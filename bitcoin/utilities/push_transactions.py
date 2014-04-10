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
# Date: 2014-03-28
#
# Get transactions from the BitStamp API and stores the relevant information (timestamp, rate, price, amount) from the
# relevant entries (exchange) in the sqlite3 database.


import sqlite3


import bitcoin
import bitcoin.client
from bitcoin.utilities import unix_timestamp


def push(log=True):
    """
    Fetches transactions from BitStamp and pushes them in to the sqlite3 database where they are used to determine the
    latest buy and sell prices.
    """

    conn = sqlite3.connect( bitcoin.get_db() )
    cursor = conn.cursor()

    if log: print("Fetching transactions from BitStamp server ...")
    data = bitcoin.client.transactions()

    if log: print("Inserting data in to 'transactions' table ...")

    for trx in data:

        ts = unix_timestamp(trx['datetime'])

        cursor.execute('''REPLACE INTO "transactions" ("time", "usd", "btc", "rate") VALUES (?,?,?,?)''', (ts, trx['usd'], trx['btc'], trx['btc_usd']))

    conn.commit()
    conn.close()

    if log: print("Done\n")