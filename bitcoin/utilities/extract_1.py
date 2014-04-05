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
# Date: 2014-03-27
#
# A script for extracting the last 2 hours of buy prices (120 samples) from the database and storing it in a file.


import sqlite3

SAMPLES = 720


if __name__ == '__main__':

    fout = open('prices.txt', 'w')

    conn = sqlite3.connect('../data.db')
    cursor = conn.cursor()

    for values in cursor.execute('''SELECT "buy" FROM (SELECT "time", "buy" FROM "prices" ORDER BY "time" DESC LIMIT ?) ORDER BY "time" ASC''', (SAMPLES,)):   # Get list of times in descending order

        fout.write("%.2f\n" % values[0])

    conn.close();
    fout.close();
