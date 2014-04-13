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
# Date: 2014-04-12
#
# Decision: Falling Trench (this is the mirror opposite of Rising Peak)
#
#   Implements the "Falling Trench" decision where-in
#
#       if we have USD balance (> 10 - the min buy amount) AND the band has NOT been activated
#       AND the avg buy price falls below a specified threshold
#
#           Then
#               create a buyng band (upper-band set to threshold and lower-band (limit order) set to 1% below current buyng price) and store it in redis
#
#
#       OR if we have USD balance and the band is active
#
#           AND buy price rises above the band-upper value
#
#               Then
#                   acquire all possible btc
#
#           AND buy price is below the last buy price
#
#               Then
#                   move the entire band down by this delta (the band is NEVER raised)


import json

from bitcoin import current_time, round2
import bitcoin.actions as actions
import bitcoin.client as client
import bitcoin.redis_client as redis_client
from bitcoin.models import Decision


# Define the necessary descriptive values:

ACTIVATION_THRESHOLD = redis_client.falling_trench_activation_threshold()       # Value below which if the avg buy price decreases the buying/trench band is activated
LOWER_LIMIT_FACTOR = redis_client.falling_trench_lower_limit_factor()          # The factor by which the buy price is multiplied to get the new lower limit of the band

REDIS_KEY = "falling_trench_band"


# Define the handle for the redis database
rds = redis_client.rds


def log(msg, newline=False):
    """
    Method for logging messages from the decision.
    """

    print("[Falling Trench] " + msg)

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

    if data.usd_balance > 10:

        band = fetch()

        if band:            # Since the data is in redis the band is active

            if data.buy > band['upper']:      # If the buy-price has risen above the band we must take action (acquire BTC)

                return True

            delta = round2(band['lower'] - data.buy * LOWER_LIMIT_FACTOR)      # Change in lower band based on the current buy price

            if delta > 0:       # If the buy price has decreased such that the band is pushed downwards we update the band (it NEVER goes up)

                band['upper'] -= delta
                band['lower'] -= delta

                log(current_time())
                log("Delta = -${}. Pushing band down to: ${} - ${}.\n".format(delta, band['lower'], band['upper']))

                push(band)

                usd = data.usd_balance
                client.cancel_all_orders()
                client.usd_buy_order(usd, round2(band['lower']))

                log("New buy order created.")

        else:               # The band is inactive

            if data.avg_buy < ACTIVATION_THRESHOLD:        # Avg Buy is below Activation Threshold so we activate the band

                log(current_time())
                log("Avg Buy price = ${} has fallen below the Activation Threshold = ${}".format(data.avg_buy, ACTIVATION_THRESHOLD), True)

                b = {'upper': ACTIVATION_THRESHOLD, 'lower': data.buy * LOWER_LIMIT_FACTOR}       # Set band values
                rds.set(REDIS_KEY, json.dumps(b))               # Convert dictionary to json string and store it in redis server

                usd = data.usd_balance
                client.cancel_all_orders()
                client.usd_buy_order(usd, round2(b['lower']))      # Set up a sell order for the upper band limit

                log("Creating band: ${} - ${}".format(b['lower'], b['upper']))

    return False


def action(data):       # Define the action to be carried out if the condition is met

    band = fetch()

    if data.buy > band['upper']:

        log("Buy price = ${} has risen above the band upper limit = ${}".format(data.buy, band['upper']))

    else:

        log("ERROR")
        return

    actions.acquire()
    delete()


decision = Decision(condition, action, True)