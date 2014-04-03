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

import common
from secrets import api



def credentials():
    """
    This method returns all of the credentials that must be send in the POST body of API requests to Bitstamp for authentication.
    """

    creds = {}

    nonce = str(int(time.time() * 1e6))       # We use the Unix timestamp in microseconds converted to a string as the nonce.
    key = api['key']
    message = nonce + api['client_id'] + key

    signature = hmac.new(api['secret'], msg=message, digestmod=hashlib.sha256).hexdigest().upper()

    creds['key'] = key
    creds['nonce'] = nonce
    creds['signature'] = signature

    return creds


def current_price():
    """
    Fetch the current buy and sell prices.
    """

    url = "https://www.bitstamp.net/api/ticker/"

    response = json.load(urllib2.urlopen(url))

    data = {'buy': response["ask"], 'sell': response["bid"]}

    return data


def balance():
    """
    Fetch the BTC and USD balance in the account.
    """

    url = "https://www.bitstamp.net/api/balance/"

    return request(url)


def transactions():
    """
    Fetch the User Transaction history.
    """

    url = "https://www.bitstamp.net/api/user_transactions/"

    return request(url)


def open_orders():
    """
    Fetch all currently open orders.
    """

    url = "https://www.bitstamp.net/api/open_orders/"

    return request(url)


def cancel_order(id):
    """
    Cancel the order with the specified id.
    """

    url = "https://www.bitstamp.net/api/cancel_order/"

    return request(url, {'id': id})


def cancel_all_orders():
    """
    Cancels ALL open orders.
    """

    data = open_orders()

    for datum in data:

        cancel_order(datum['id'])


def buy_order(amount, price):
    """
    Create a Buy Limit order.
    """

    url = "https://www.bitstamp.net/api/buy/"

    return request(url, {'amount': amount, 'price': price})


def sell_order(amount, price):
    """
    Create a Sell Limit order.
    """

    url = "https://www.bitstamp.net/api/sell/"

    return request(url, {'amount': amount, 'price': price})


def purge():
    """
    Method for selling all BTC as quickly as possible.
    """

    print("Beginning purge")

    flag = True

    while flag:

        btc = float(balance()['btc_balance'])      # No. of BTC still in account

        if btc > 0:

            print("Remaining BTC: {}".format(btc))
            cancel_all_orders()

            sell_price = current_price()['sell']
            sell_order(btc, sell_price)

            time.sleep(5)           # Wait for 5 seconds before continuing

        else:

            flag = False        # Break while loop
            print("Purge ends.\n")


def acquire():
    """
    Method for acquiring all BTC as quickly as possible.
    """

    print("Beginning acquire")

    flag = True

    while flag:

        usd = float(balance()['usd_balance'])      # Amount of USD still in account

        if usd > 0:

            print("Remaining USD: {}".format(usd))
            cancel_all_orders()

            buy_price = current_price()['buy']
            btc = common.chop_btc(usd / buy_price)

            print("Buying BTC: {}", btc)

            buy_order(btc, buy_price)

            time.sleep(5)           # Wait for 5 seconds before continuing

        else:

            flag = False        # Break while loop
            print("Acquire ends.\n")



def request(url, payload={}):
    """
    Uses the BitStamp REST API to POST a request and get the response back as a Python Dictionary.

    We pass in a dictionary payload containing data above and beyond the credentials.
    """

    pd = credentials()      # Initial payload is the credentials dictionary
    pd.update(payload)      # We add the passed in dictionary to the data object we send in the request.

    data = urllib.urlencode( pd )

    fin = urllib2.urlopen(url, data)
    jResponse = fin.readlines()

    response = json.loads( jResponse[0] )

    if type(response) == dict and 'error' in response.keys():

        raise ClientException("API Error: " + str(response['error']))

    return response



class ClientException(Exception):
    """
    Custom exception raised when an error occurs during the client's operation.
    """

    def __init__(self, message):

        super(ClientException, self).__init__(message)
