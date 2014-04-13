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


from bitcoin.models import Data

import bitcoin.decisions.absolute_zero as absolute_zero
import bitcoin.decisions.minimize_loss as minimize_loss
import bitcoin.decisions.minimum_profit as minimum_profit
import bitcoin.decisions.rising_peak as rising_peak
import bitcoin.decisions.falling_trench as falling_trench


def initiate_decisions():
    """
    We create a list of decisions that need to be made to carry out the OODA cycle.
    """

    decisions = []

    decisions.append( absolute_zero.decision )
    decisions.append( minimize_loss.decision )
    decisions.append( minimum_profit.decision )
    decisions.append( rising_peak.decision )
    decisions.append( falling_trench.decision )

    return decisions



if __name__ == '__main__':

    d = Data()

    # Create the list of decisions to be carried out (this includes the Orient, Decide and Act phases of OODA)
    decisions = initiate_decisions()


    for decision in decisions:

        decision.execute(d)
        
        if decision.final():

            break
