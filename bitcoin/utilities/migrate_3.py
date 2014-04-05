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
# This script reads in all the "time" values in the "prices" table and calculates the timestamp where the gaps between successive timestamps is greater than 60 seconds in preparation for dropping values with larger gaps.


import sqlite3
import time


if __name__ == '__main__':

    conn = sqlite3.connect('../data.db')
    cursor = conn.cursor()

    prev = int(time.time())
    current = 0

    count = 0

    for values in cursor.execute('''SELECT "time" FROM "prices" ORDER BY "time" DESC'''):   # Get list of times in descending order

        count += 1
        current = values[0]

        if (prev - current) > 270:       # If the gap is greater than 90 seconds we have found the first gap so we print and exit

            print current
            break

        prev = current      # Update prev value
