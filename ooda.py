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


import datetime
import rpy2.robjects as robjects
import sqlite3
import time

import client
import utilities.push_transactions


def max_price(prices):
    """
    Function that uses R to find the maximum price from a list of float prices.
    """

    return robjects.r['max'](prices)[0]        # We use the R object to access the 'max' function, pass in the list of prices and then get the 1st element to get the result


def format_time(t):
    """
    Method for converting a unix epoch timestamp to human-readable format.
    """

    return datetime.datetime.fromtimestamp(t).strftime("%m-%d %H:%M")


def current_time():
    """
    Method for getting the current time in a human-readable format.
    """

    return datetime.datetime.fromtimestamp(time.time()).strftime("%m-%d %H:%M")


class Data:
    """
    This class encapsulates the data collected and as such is representative of the current STATE of bitcoin prices, including history.
    """

    def __init__(self):
        """
        Initialization method. Here is where we poll the database and the BitStamp API to collect relevant data.
        """
        # The first step is to fetch current price data from the sqlite3 database

        #filepath = os.path.join(os.path.dirname(__file__), 'data.db')

        conn = sqlite3.connect('/home/abid/scripts/python/bitcoin/data.db')
        cursor = conn.cursor()

        values = cursor.execute('''SELECT "time", "buy", "sell" FROM "prices" ORDER BY "time" DESC LIMIT 1''').fetchone()

        self.time = values[0]
        self.buy = values[1]
        self.sell = values[2]

        # Use BitStamp API client to fetch the USD and BTC balance
        bal = client.balance()

        self.usd_balance = bal['usd_balance']
        self.btc_balance = bal['btc_balance']

        # Query "transactions" table to database to get the latest buy and sell prices and the times they occurred (needed for orienting/analysis)
        values = cursor.execute('''SELECT "time", "rate" FROM "transactions" WHERE "usd" > 0 ORDER BY "time" DESC LIMIT 1''').fetchone()
        self.last_sell_time = values[0]
        self.last_sell_price = values[1]

        values = cursor.execute('''SELECT "time", "rate" FROM "transactions" WHERE "usd" < 0 ORDER BY "time" DESC LIMIT 1''').fetchone()
        self.last_buy_time = values[0]
        self.last_buy_price = values[1]

        # Fetch all buy prices since the last time BTC was sold
        self.buy_prices = []
        for values in cursor.execute('''SELECT "buy" FROM "prices" WHERE "time" > ?''', (self.last_sell_time,)):

            self.buy_prices.append(values[0])

        # Fetch all sell prices since the last time BTC was bought
        self.sell_prices = []
        for values in cursor.execute('''SELECT "sell" FROM "prices" WHERE "time" > ?''', (self.last_buy_time, )):

            self.sell_prices.append(values[0])

        # Convert array of prices in to R vectors
        self.buy_prices = robjects.FloatVector(self.buy_prices)
        self.sell_prices = robjects.FloatVector(self.sell_prices)

        cursor.close()

        # Carry out Debug tasks to change Date object for debugging:


    def __str__(self):
        """
        String representation of the object.
        """
        return "Timestamp: {ts}\n\nBuy: {buy}\nSell: {sell}\n\nUSD Balance: {usd}\nBTC Balance: {btc}\n\nLast Buy Price: {obuy}  {obtime}\nLast Sell Price: {osell}  {ostime}\n\nBuy Prices: {bprices}\nSell Prices: {sprices}".format(ts=format_time(self.time), buy=self.buy, sell=self.sell, usd=self.usd_balance, btc=self.btc_balance, obuy=self.last_buy_price, osell=self.last_sell_price, bprices=self.buy_prices, sprices=self.sell_prices, obtime=format_time(self.last_buy_time), ostime=format_time(self.last_sell_time))



class Decision:
    """
    This class models a "decision" in which the data is tested for a condition and if the condition is met an action is performed. Additionally the Decision can be labelled such that if the condition is met no further decisions need to make (a finality is associated with it).
    """

    def __init__(self, condition, action, final):
        """
        The Decision object is initialized by passing in the condition function that runs the test the action function to run if the test is successful and the 'final' boolean which indicates if this decision is a final one (no more decisions need to be made if this one tests true).
        """

        self.condition = condition
        self.action = action
        self._final = final

        self._condition = False     # Internal flag to determine if the condition test was true or false


    def execute(self, data):
        """
        Carry out the decision that is test the data and if true carry out the required action.
        """

        self._condition = self.condition(data)

        if (self._condition):

            self.action(data)


    def final(self):
        """
        Returns True only if the condition was met and the final flag was set initially. This indicates that this was the final decision and no more decisions need to be made
        """

        return self._condition and self._final



def initiate_decisions():
    """
    We create a list of decisions that need to be made to carry out the OODA cycle.
    """

    decisions = []

    # If we have BTC and the sell price falls below 2.5% of the original (last) buy price the BTC must be sold immediately in anticipation of an upcoming slump.
    def condition(data):

        if data.btc_balance > 0:

            if data.sell < 0.975 * data.last_buy_price:

                print(current_time())
                print("Original Buy Price: {obuy} - Current Sell Price: {sell} - Delta: {delta} - %age: {pct}".format(obuy=data.last_buy_price, sell=data.sell, delta=data.sell - data.last_buy_price, pct=(data.sell - data.last_buy_price)/data.last_buy_price * 100))

                return True

        return False

    def action(data):

        print("BTC sell price has fallen below 97.5% of original buy price. Selling.\n")

        ## The first step is to cancel all open orders:
        #client.cancel_all_orders()
        #
        ## Next we create a sell order for all the BTC:
        #client.sell_order(data.btc_balance, 0.975 * data.last_buy_price)

        # We are in a rush to off-load so we purge all BTC
        #client.purge()

        # Push transactions in to database to update it
        #utilities.push_transactions.push()


    decisions.append( Decision(condition, action, True) )


    # If we have BTC and the sell price is between 100% and 102% of the original (last) buy price the BTC should be sold if the price has fallen from above 101% ensuring that a minimum profit will be earned.
    def condition(data):

        if data.btc_balance > 0:

            if data.last_buy_price < data.sell < 1.02 * data.last_buy_price:

                if max_price(data.sell_prices) > 1.02 * data.last_buy_price:     # The sell prices exceeded the upper threshold before dropping thereby meeting the condition

                    print("Original Buy Price: {obuy} - Current Sell Price: {sell} - Delta: {delta} - %age: {pct}".format(obuy=data.last_buy_price, sell=data.sell, delta=data.sell - data.last_buy_price, pct=(data.sell - data.last_buy_price) / data.last_buy_price * 100))
                    print("Max Sell price: {}".format(max_price(data.sell_prices)))

                    return True

        return False

    def action(data):

        print("BTC sell price is between 100% and 102% of original buy price.\n")

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
