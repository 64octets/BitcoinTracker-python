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
# Date: 2014-04-10
#
# Decision: Rising Peak
#
#   Implements the "Rising Peak" decision where-in
#
#       if we have BTC balance and the band has NOT been activated
#       the avg sell price rises above a specified threshold
#
#           Then
#               create a selling band (lower-band set to threshold and upper-band (limit order) set to 1% above current selling price) and store it in redis
#
#
#       OR if we have BTC balance and the band is active
#
#           AND sell price falls below the band-lower value
#
#               Then
#                   purge all btc
#
#           AND sell price is above the last price
#
#               Then
#                   move the entire band up by this delta (the band is NEVER lowered)


import json
import redis

from bitcoin import current_time, round2
import bitcoin.actions as actions
import bitcoin.client as client
from bitcoin.models import Decision


# Define the necessary descriptive values:

ACTIVATION_THRESHOLD = 432         # Value above which if the avg sell price increases the selling/peak band is activated
UPPER_LIMIT_FACTOR = 1.01          # The factor by which the sell price is multiplied to get the new upper limit of the band

REDIS_KEY = "rising_peak_band"


# Define the handle for the redis database
rds = redis.StrictRedis(host='localhost', port=6379, db=0)


def log(msg, newline=False):
    """
    Method for logging messages from the decision.
    """

    print("[Rising Peak] " + msg)

    if newline: print    # If the flag is set print a new line


def fetch():
    """
    Method for fetching band dictionary from redis.
    """
    band_string = rds.get(REDIS_KEY)

    if band_string:

        return json.loads(band_string)

    else:
        return None     # None is returned if the key doesn't exist in redis


def push(band):
    """
    Method for placing band dictionary in redis.
    """
    rds.set(REDIS_KEY, json.dumps(band))


def delete():
    """
    Method for deleting the band dictionary from redis.
    """
    rds.delete(REDIS_KEY)



def condition(data):        # Define the condition function of the Decision

    if data.btc_balance > 0:

        band = fetch()

        if band:            # Since the data is in redis the band is active

            if data.sell < band['lower']:      # If the sell-price has fallen below the band we must take action

                return True

            delta = round2(data.sell * UPPER_LIMIT_FACTOR - band['upper'])      # Change in upper band based on the current sell price

            if delta > 0:       # If the sell price has increased such that the band is pushed upwards we update the band (it NEVER goes down)

                band['upper'] += delta
                band['lower'] += delta

                log(current_time())
                log("Delta = ${}. Pushing band up to: ${} - ${}.\n".format(delta, band['lower'], band['upper']))

                push(band)

                btc = client.btc()
                client.cancel_all_orders()
                client.sell_order(btc, round2(band['upper']))

                log("New sell order created.")

        else:               # The band is inactive

            if data.avg_sell > ACTIVATION_THRESHOLD:        # Avg Sell is above Activation Threshold so we activate the band

                log(current_time())
                log("Avg Sell price = ${} has risen above the Activation Threshold = ${}".format(data.avg_sell, ACTIVATION_THRESHOLD), True)

                b = {'lower': ACTIVATION_THRESHOLD, 'upper': data.sell * UPPER_LIMIT_FACTOR}       # Set band values
                rds.set(REDIS_KEY, json.dumps(b))               # Convert dictionary to json string and store it in redis server

                btc = client.btc()
                client.cancel_all_orders()
                client.sell_order(btc, round2(b['upper']))      # Set up a sell order for the upper band limit

    return False


def action(data):       # Define the action to be carried out if the condition is met

    band = fetch()

    if data.sell < band['lower']:

        log("Sell price = ${} has fallen below the band lower limit = ${}".format(data.sell, band['lower']))

    else:

        log("ERROR")
        return

    actions.purge()
    delete()


decision = Decision(condition, action, True)