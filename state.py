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
# Date: 2014-04-08
#
# This script prints a summary of the current state of the BitStamp account, basically displaying the current balance
# prices and open orders


import bitcoin.client as client


if __name__ == '__main__':

    print("\nCurrent Price:\n")
    print(client.current_price())

    print("\n\nBalance:\n")
    print(client.balance())

    print("\n\nOpen Orders:\n")
    print(client.open_orders())

    print