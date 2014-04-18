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
# Date: 2014-04-17
#
# This module implements utilities for calculating the moving average of a data series.


def moving_average(series, N):
    """
    Calculates the Weighted Moving Average of a series over the last N values using a linear weighing function.
    """
    weighing_function = lambda x: (N - x)       # We define a linear weighing function over N samples

    weighted_series = []

    for ii in range(len(series)):

        sum = 0
        denom = 0

        for jj in range(N):

            if (ii - jj) < 0:

                break

            sum += series[ii - jj] * weighing_function(jj)       # Multiply value by weight calculated accordingly to distance from main value
            denom += weighing_function(jj)

        weighted_series.append( round( sum / float(denom), 2) )     # Append the calculated weighted sum (rounded to 2 decimal places) to the output series

    return weighted_series



def latest_moving_average(series, N):
    """
    Calculates the linearly weighed moving average of the last sample in the series using the previous (N-1) samples.
    """
    weighing_function = lambda x: (N - x)

    sum = 0
    denom = 0

    for ii in range(N):

        sum += series[ii] * weighing_function(ii)
        denom += weighing_function(ii)

    return round( sum / float(denom), 2 )