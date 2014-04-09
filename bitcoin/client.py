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

import bitcoin
from bitcoin import settings
from bitcoin.secrets import api


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
    prev_sell_price = 1e9           # A very large number so that the condition is triggered the first time.

    while flag:

        btc = float(balance()['btc_balance'])      # No. of BTC still in account

        if btc > 0:

            print("Remaining BTC: {}".format(btc))
            print("Previous sell price: {}".format(prev_sell_price))

            sell_price = float(current_price()['sell'])
            print("Current sell price: {}".format(sell_price))

            if sell_price < settings.SELL_PRICE_DROP_FACTOR * prev_sell_price:            # The sell price has fallen and so the previous sell price will NOT trigger an actual sale (because of the way limit orders work) so we create a new order

                cancel_all_orders()

                sell_order(btc, sell_price)
                prev_sell_price = sell_price        # Update prev_sell_price for later comparison

            elif sell_price > settings.SELL_PRICE_RISE_FACTOR * prev_sell_price:

                print("Sell price has increased to a factor of {}. Cancelling purge".format(settings.SELL_PRICE_RISE_FACTOR))
                cancel_all_orders()
                return

            # NOTE: If the sell_price doesn't fall by more than DROP_FACTOR or rise by more than RISE_FACTOR we keep the same sell order active.

            time.sleep(settings.TRANSACTION_INTERVAL)           # Wait for specified interval to allow sale to occur before continuing

        else:

            flag = False        # Break while loop
            print("All BTC sold. Purge ends.\n")


def acquire():
    """
    Method for acquiring all BTC as quickly as possible.
    """

    print("Beginning acquire")
    prev_buy_price = 0                  # A very small number so that the condition is triggered the first time.

    flag = True

    while flag:

        bal = balance()
        usd = float(bal['usd_balance'])      # Amount of USD still in account
        fee = float(bal['fee'])              # %age of cost taken as transaction fee 
        amount = bitcoin.adjusted_usd_amount(usd, fee)     # Amount of USD that can be used to buy BTC once the fee has been subtracted

        if usd > 0.10:      # The way the fee is subtract a very small amount of usd might be left behind which we ignore

            print("Remaining USD: {}".format(usd))
            print("Previous buy price: {}".format(prev_buy_price))

            buy_price = float(current_price()['buy'])
            btc = bitcoin.chop_btc(amount / buy_price)              # Calculate the correctly floored (rounded) amount of btc that can be bought at the current buy price

            print("Current buy price: {}".format(buy_price))
            print("Fee %age: {}".format(fee))
            print("Buying BTC: {}".format(btc))

            if buy_price > settings.BUY_PRICE_RISE_FACTOR * prev_buy_price:

                cancel_all_orders()

                buy_order(btc, buy_price)
                prev_buy_price = buy_price

            elif buy_price < settings.BUY_PRICE_DROP_FACTOR * prev_buy_price:

                print("Buy price has dropped to a factor of {}. Cancelling acquire.".format(settings.BUY_PRICE_DROP_FACTOR))
                cancel_all_orders()
                return

            # NOTE: If the buy_price doesn't fall by more than DROP_FACTOR or rise by more than RISE_FACTOR we keep the same sell order active.

            time.sleep(settings.TRANSACTION_INTERVAL)           # Wait for 5 seconds before continuing

        else:

            flag = False        # Break while loop
            print("All USD spent. Acquire ends.\n")


def buy_for_usd(usd):
    """
    Buys BTC at the current buy price for the specified amount inclusive of fees charged. So the exact amount specified
    is bought.
    """

    buy_price = float(current_price()['buy'])       # Fetch current buy price

    usd_buy_order(usd, buy_price)


def usd_buy_order(usd, price):
    """
    Places a Buy Order for BTC at the specified price and such that the BTC bought costs the specified amount of USD,
    taking the fee in to account.

    So you can place a buy order for $1200 worth of BTC at $510.
    """

    fee = float(balance()['fee'])
    amount = bitcoin.adjusted_usd_amount(usd, fee)

    btc = bitcoin.chop_btc(amount / price)

    print("Buying {} btc at ${} at a cost of ${}".format(btc, price, usd))

    buy_order(btc, price)


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
