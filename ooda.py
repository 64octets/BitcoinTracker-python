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
# Date: 2014-02-27
#
# Implement the OODA loop (Observe-Orient-Decide-Act) for bitcoin exchange.


import client
from models import Data, Decision
import utilities.push_transactions

from common import max_price, current_time, format_time


def initiate_decisions():
    """
    We create a list of decisions that need to be made to carry out the OODA cycle.
    """

    decisions = []

    # If we have BTC and the sell price falls below 2% of the original (last) buy price the BTC must be sold immediately in anticipation of an upcoming slump.
    def condition(data):

        if data.btc_balance > 0:

            if data.sell < 0.98 * data.last_buy_price:

                print("Original Buy Price: {obuy} - Current Sell Price: {sell} - Delta: {delta} - %age: {pct}".format(obuy=data.last_buy_price, sell=data.sell, delta=data.sell - data.last_buy_price, pct=(data.sell - data.last_buy_price)/data.last_buy_price * 100))

                return True

        return False

    def action(data):

        print("{}\nBTC sell price has fallen below 98% of original buy price. Selling.\n".format(current_time()))

        ## The first step is to cancel all open orders:
        #client.cancel_all_orders()
        #
        ## Next we create a sell order for all the BTC:
        #client.sell_order(data.btc_balance, 0.975 * data.last_buy_price)

        # We are in a rush to off-load so we purge all BTC
        client.purge()

        # Push transactions in to database to update it
        utilities.push_transactions.push()


    decisions.append( Decision(condition, action, True) )


    # If we have BTC and the sell price is between 100.8% and 102% of the original (last) buy price the BTC should be sold if the price has fallen from above 102% ensuring that a minimum profit will be earned.
    # The 100.8% comes from the fact that the fees per transaction are approximately below 0.4%. Selling below this level will cause a loss to occur.
    def condition(data):

        if data.btc_balance > 0:

            if 1.008 * data.last_buy_price < data.sell < 1.02 * data.last_buy_price:

                if max_price(data.sell_prices) > 1.02 * data.last_buy_price:     # The sell prices exceeded the upper threshold before dropping thereby meeting the condition

                    print("Original Buy Price: {obuy} - Current Sell Price: {sell} - Delta: {delta} - %age: {pct}".format(obuy=data.last_buy_price, sell=data.sell, delta=data.sell - data.last_buy_price, pct=(data.sell - data.last_buy_price) / data.last_buy_price * 100))
                    print("Max Sell price: {}".format(max_price(data.sell_prices)))

                    return True

        return False

    def action(data):

        print("{}\nBTC sell price is between 100.8% and 102% of original buy price and the Max Price has exceeded 102% earlier.\n".format(current_time()))

        #purge()

        #client.cancel_all_orders()
        #client.sell_order(data.btc_balance, data.sell)

        ## Push transactions in to database to update it
        #utilities.push_transactions.push()


    decisions.append( Decision(condition, action, True) )

    return decisions




if __name__ == '__main__':

    d = Data()

    # Create the list of decisions to be carried out (this includes the Orient, Decide and Act phases of OODA)
    decisions = initiate_decisions()


    for decision in decisions:

        decision.execute(d)
        
        if decision.final():

            break
