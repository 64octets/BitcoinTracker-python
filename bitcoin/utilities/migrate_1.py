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
# Date: 2014-03-12
#
# This script reads data from the data.txt file and writes it in to the data.db sqlite3 database.
# Hence it is a migration script.


import sqlite3


if __name__ == '__main__':

    fin = open("../data.txt")
    conn = sqlite3.connect('../data.db')
    cursor = conn.cursor()

    for line in fin.readlines():            # Read in from the file a line at a time

        values = line.split()               # Extract values from the line and cast them to the correct type

        time = int(values[0])
        buy = float(values[1])
        sell = float(values[2])

        cursor.execute('''REPLACE INTO "prices" ("time", "buy", "sell") VALUES (?, ?, ?)''', (time, buy, sell))         # Insert or Replace data in to database using recommended parameter substitution

    conn.commit()       # Commit changes
    conn.close()        # Close connection

    fin.close()




