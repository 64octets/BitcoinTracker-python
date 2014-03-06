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
# This script fetches data from the coinbase.com backedn API and prints it to stdout

import urllib2
import json
import time

BUY_URL = "https://coinbase.com/api/v1/prices/buy"
SELL_URL = "https://coinbase.com/api/v1/prices/sell"


def main():

    buy = json.load(urllib2.urlopen(BUY_URL))['total']['amount']

    sell = json.load(urllib2.urlopen(SELL_URL))['total']['amount']

    now = int(time.time())        # Get current unix time

    print("{} {} {}".format(now, buy, sell))


main()