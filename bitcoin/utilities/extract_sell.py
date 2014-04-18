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
# Date: 2014-04-02
#
# A script for extracting the last 6 hours of sell prices (6 * 60 samples) from the database and storing it in a file.


import sqlite3

import bitcoin

SAMPLES = 6 * 60


if __name__ == '__main__':

    fout = open('sell.txt', 'w')

    conn = sqlite3.connect(bitcoin.get_db())
    cursor = conn.cursor()

    for values in cursor.execute('''SELECT "sell" FROM (SELECT "time", "sell" FROM "prices" ORDER BY "time" DESC LIMIT ?) ORDER BY "time" ASC''', (SAMPLES,)):   # Get list of times in descending order

        fout.write("%.2f\n" % float(values[0]))

    conn.close();
    fout.close();
