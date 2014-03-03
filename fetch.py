#! /usr/bin/python

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