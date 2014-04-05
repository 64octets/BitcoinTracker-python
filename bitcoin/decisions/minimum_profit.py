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
# Date: 2014-04-04
#
# Decision: Minimum Profit
#
#   Implements the "Minimum Profit" decision where-in
#
#       if we have BTC balance and
#       the sell price exceeds and returns to a narrow band above the original buy price
#
#   Then
#       Cancel all open orders
#       Purge all BTC (in the hopes of making a small profit - that cancels the fee)


import bitcoin.client as client
import bitcoin.utilities.push_transactions as push_transactions
from bitcoin.common import current_time, max_price
from bitcoin.models import Decision


# Define the necessary descriptive values:

BAND_UPPER = 1.02       # Upper bound of band is 2% above the original buy price
BAND_LOWER = 1.008      # Lower bound is 0.8% above the orig. buy price (considering the fee to be about 0.4% for both the buy and the sell)



def log(msg):
    """
    Method for logging messages from the decision.
    """

    print("[Minimum Profit] " + msg)



def condition(data):

    if data.btc_balance > 0:

        if BAND_LOWER * data.last_buy_price < data.sell < BAND_UPPER * data.last_buy_price:

            if max_price(data.sell_prices) > BAND_UPPER * data.last_buy_price:      # The sell prices exceeded the upper
                                                                                    # threshold before dropping

                log("Orig. Buy Price: {obuy} - Curr. Sell Price: {sell} - Delta: {delta} - %age: {pct}".format(obuy=data.last_buy_price, sell=data.sell, delta=data.sell - data.last_buy_price, pct=(data.sell - data.last_buy_price) / data.last_buy_price * 100))

                log("Max Sell price: {}".format(max_price(data.sell_prices)))

                return True

    return False


def action(data):

    log("{}\nBTC sell price is between {}% and {}% of orig. buy price and the Max Sell Price to date exceeds {}%.\n".format(current_time(), BAND_LOWER, BAND_UPPER, BAND_UPPER))

    client.purge()

    push_transactions.push()


decision = Decision(condition, action, True)