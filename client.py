# Author: Abid H. Mujtaba
# Date: 2014-03-24
#
# This module implements a client that communicates with BitStamp using the specified API.

import hashlib
import hmac
import json
import time
import urllib
import urllib2

from secrets import api


def credentials():
    """
    This method returns all of the credentials that must be send in the POST body of API requests to Bitstamp for authentication.
    """

    creds = {}

    nonce = str(int(time.time()))       # We use the Unix timestamp in seconds converted to a string as the nonce.
    key = api['key']
    message = nonce + api['client_id'] + key

    signature = hmac.new(api['secret'], msg=message, digestmod=hashlib.sha256).hexdigest().upper()

    creds['key'] = key
    creds['nonce'] = nonce
    creds['signature'] = signature

    return creds


def balance():
    """
    Fetch the BTC and USD balance in the account.
    """

    url = "https://www.bitstamp.net/api/balance/"

    return request(url)


def request(url):
    """
    Uses the BitStamp REST API to POST a request and get the response back as a Python Dictionary
    """

    data = urllib.urlencode( credentials() )

    fin = urllib2.urlopen(url, data)
    response = fin.readlines()

    return json.loads( response[0] )


def balance_usd():

    return float( balance()['usd_available'] )


def balance_btc():

    return float( balance()['btc_available'] )
