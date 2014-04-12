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
# Date: 2014-04-11
#
# Implements various actions that are called both internally and externally. They are placed here to avoid circular imports since they call on methods from all over the place and in turn are called from all over.


import time

import bitcoin
import bitcoin.client as client
import bitcoin.settings as settings


def purge():
    """
    Method for selling all BTC as quickly as possible.
    """

    print("Beginning purge")

    flag = True
    prev_sell_price = 1e9           # A very large number so that the condition is triggered the first time.

    while flag:

        btc = float(client.balance()['btc_balance'])      # No. of BTC still in account

        if btc > 0:

            print("Remaining BTC: {}".format(btc))
            print("Previous sell price: {}".format(prev_sell_price))

            sell_price = float(client.current_price()['sell'])
            print("Current sell price: {}".format(sell_price))

            if sell_price < settings.SELL_PRICE_DROP_FACTOR * prev_sell_price:            # The sell price has fallen and so the previous sell price will NOT trigger an actual sale (because of the way limit orders work) so we create a new order

                client.cancel_all_orders()

                client.sell_order(btc, sell_price)
                prev_sell_price = sell_price        # Update prev_sell_price for later comparison

            elif sell_price > settings.SELL_PRICE_RISE_FACTOR * prev_sell_price:

                print("Sell price has increased to a factor of {}. Cancelling purge".format(settings.SELL_PRICE_RISE_FACTOR))
                client.cancel_all_orders()
                return

            # NOTE: If the sell_price doesn't fall by more than DROP_FACTOR or rise by more than RISE_FACTOR we keep the same sell order active.

            time.sleep(settings.TRANSACTION_INTERVAL)           # Wait for specified interval to allow sale to occur before continuing

        else:

            import bitcoin.decisions.rising_peak as rising_peak     # We import here to avoid a circular import

            flag = False        # Break while loop
            rising_peak.delete()        # Clear Redis information about band since the BTC has been purged

            print("All BTC sold. Purge ends.\n")


def acquire():
    """
    Method for acquiring all BTC as quickly as possible.
    """

    print("Beginning acquire")
    prev_buy_price = 0                  # A very small number so that the condition is triggered the first time.

    flag = True

    while flag:

        bal = client.balance()
        usd = float(bal['usd_balance'])      # Amount of USD still in account
        fee = float(bal['fee'])              # %age of cost taken as transaction fee
        amount = bitcoin.adjusted_usd_amount(usd, fee)     # Amount of USD that can be used to buy BTC once the fee has been subtracted

        if usd > 1:      # BitStamp requires at least a $1 order (some small amount might be left once fees are calculated)

            print("Remaining USD: {}".format(usd))
            print("Previous buy price: {}".format(prev_buy_price))

            buy_price = float(client.current_price()['buy'])
            btc = bitcoin.chop_btc(amount / buy_price)              # Calculate the correctly floored (rounded) amount of btc that can be bought at the current buy price

            print("Current buy price: {}".format(buy_price))
            print("Fee %age: {}".format(fee))
            print("Buying BTC: {}".format(btc))


            if buy_price != prev_buy_price:       # If the buy price has changed we update the buy_order to ensure a quick acquire.

                client.cancel_all_orders()

                client.buy_order(btc, buy_price)
                prev_buy_price = buy_price

            time.sleep(settings.TRANSACTION_INTERVAL)           # Wait for 5 seconds before continuing

        else:

            flag = False        # Break while loop
            print("All USD spent. Acquire ends.\n")