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
import os
import sqlite3

from client import balance


class Data:
    """
    This class encapsulates the data collected and as such is representative of the current STATE of bitcoin prices, including history.
    """

    def __init__(self):
        """
        Initialization method. Here is where we poll the database and the BitStamp API to collect relevant data.
        """
        # The first step is to fetch current price data from the sqlite3 database

        filepath = os.path.join(os.path.dirname(__file__), 'data.db')

        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()

        values = cursor.execute('''SELECT "time", "buy", "sell" FROM "prices" ORDER BY "time" DESC LIMIT 1''').fetchone()

        self.time = values[0]
        self.buy = values[1]
        self.sell = values[2]

        cursor.close()

        # Use BitStamp API client to fetch the USD and BTC balance
        bal = balance()

        self.usd_balance = bal['usd_available']
        self.btc_balance = bal['btc_available']

        # Carry out Debug tasks to change Date object for debugging:
        self.original_buy = 510



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

            self.action()


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

    # If we have BTC and the sell price falls 0.5% of the original buy price the BTC must be sold immediately in anticipation of an upcoming slump.
    def condition(data):

        if data.btc_balance > 0:

            if data.sell < 0.995 * data.original_buy:

                print("Original Buy Price: {obuy} - Current Sell Price: {sell} - Delta: {delta} - %age: {pct}".format(obuy=data.original_buy, sell=data.sell, delta=data.sell - data.original_buy, pct=(data.sell - data.original_buy)/data.original_buy*100))

                return True

        return False

    def action():

        print("BTC sell price has fallen below 99.5% of original buy price.")

    
    decisions.append( Decision(condition, action, True) )


    return decisions




if __name__ == '__main__':

    d = Data()

    # Create the list of decisions to be carried out (this includes the Orient, Decide and Act phases of OODA)
    decisions = initiate_decisions()

    formatted_time = datetime.datetime.fromtimestamp(d.time).strftime("%m-%d %H:%M")

    print "Timestamp: {ts}\n\nBuy: {buy}\nSell: {sell}\n\nUSD Balance: {usd}\nBTC Balance: {btc}\n\nOriginal Buy Price: {obuy}\n".format(ts=formatted_time, buy=d.buy, sell=d.sell, usd=d.usd_balance, btc=d.btc_balance, obuy=d.original_buy)


    for decision in decisions:

        decision.execute(d)
        
        if decision.final():

            print("Final Decision")
            break
