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
# Decision: Absolute Zero
#
#   Implements the "Absolute Zero" decision where-in
#
#       if we have BTC balance and
#       the sell price falls below the specified minimum level
#
#   Then
#       Cancel all open orders
#       Purge all BTC


import common

common.add_parent_to_path()

import bitcoin.client as client
import bitcoin.utilities.push_transactions as push_transactions
from bitcoin.models import Decision


# Define the necessary descriptive values:

MINIMUM_THRESHOLD = 400         # Min value below which if the sell-price falls the purge should be initiated


def log(msg):
    """
    Method for logging messages from the decision.
    """

    print("[Absolute Zero] " + msg)


def condition(data):        # Define the condition function of the Decision

    if data.btc_balance > 0:

        if data.sell < MINIMUM_THRESHOLD:

            log("Sell price = ${} has fallen below the Min. Threshold = ${}".format(data.sell, MINIMUM_THRESHOLD))

            return True

    return False


def action(data):       # Define the action to be carried out if the condition is met

    client.purge()      # Purge all BTC

    push_transactions.push()      # Push transactions to database


decision = Decision(condition, action, True)