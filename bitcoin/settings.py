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
# Date: 2014-04-03
#
# Implements the various settings/values used to make determinations during the decision-making phase of the OODA cycle.


# We set the margin within which the sell price is NOT changed in a purge.

SELL_PRICE_DROP_FACTOR = 99.75 / 100            # The percentage of the sell price to which if it drops the purge needs to reset to the sell price.
SELL_PRICE_RISE_FACTOR = 100.5 / 100            # The pecerntage of the sell price to which if it rises the purge is cancelled so that the price can be re-analyzed on the next OODA cycle.

# We set the margin within which the buy price is NOT changed in an acquire.

BUY_PRICE_DROP_FACTOR = 99.5 / 100              # The %age of the buy price to which if it drop the acquire is cancelled and the price can be re-analyzed on the next OODA cycle.
BUY_PRICE_RISE_FACTOR = 100.25 / 100            # The %age of the buy price to which if it rises the acquire needs to reset to the new buy price otherwise we will be unable to buy btc.


TRANSACTION_INTERVAL = 10           # The interval in seconds between updating the order in a purge or acquire

# The number of samples used to calculate the short and long moving averages:

SMA_SAMPLES = 60
LMA_SAMPLES = 120