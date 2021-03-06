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
# Decision: Minimize Loss
#
#   Implements the "Minimize Loss" decision where-in
#
#       if we have BTC balance and
#       the sell price falls below 98% of the price at which the BTC was bought (indicating mounting losses)
#
#   Then
#       Cancel all open orders
#       Purge all BTC
#
#   This decision is final (it overrides all remaining decisions).


from bitcoin import current_time
import bitcoin.actions as actions
from bitcoin.models import Decision
import bitcoin.redis_client as redis_client


# Define the necessary descriptive values:

DROP_FACTOR = redis_client.minimize_loss_drop_factor()      # The factor of the original buy price below which the sell price must fall to trigger this
                        # condition.


def log(msg, newline=False):
    """
    Method for logging messages from the decision.
    """

    print("[Minimize Loss] " + msg)

    if newline: print


# If we have BTC and the sell price falls below 2% of the original (last) buy price the BTC must be sold immediately in
# anticipation of an upcoming slump.
def condition(data):

    if redis_client.active_minimize_loss() and data.btc_balance > 0:

        if data.sell < DROP_FACTOR * data.last_buy_price:

            log(current_time())
            log("Original Buy Price: {obuy} - Current Sell Price: {sell} - Delta: {delta} - %age: {pct}".format(obuy=data.last_buy_price, sell=data.sell, delta=data.sell - data.last_buy_price, pct=(data.sell - data.last_buy_price)/data.last_buy_price * 100))

            return True

    return False


def action(data):

    if redis_client.active_minimize_loss():

        log("BTC sell price has fallen below a factor of {} of original buy price. Selling.\n".format(DROP_FACTOR), True)

        actions.purge()      # We are in a rush to off-load so we purge all BTC


decision = Decision(condition, action, True)
