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
# Date: 2014-03-20
#
# This module implements utilities for calculating the weighted average of a data series.


NUM_WEIGHING_SAMPLES = 10      # Define the weighted sum sampling window to be 15 min

WEIGHING_FUNCTION = lambda x: (NUM_WEIGHING_SAMPLES - x)           # We use a linear weighing function. x = 0 is the end-value
                                                                   # and as x increases we are looking at successively older values


def weighted_running_average(series, N, weighing_function = None):
    """
    Calculates the Weighted Running Average of a series over the last N values using the specified weighing_funciton.
    """

    if not weighing_function:       # No weighing function provided so we specify the default one

        weighing_function = lambda x: 1       # Standard mean over N values. NOTE: If you set N = 1 you get the exact value back

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



def single_weighted_average(series, N, weighing_function = None):
    """
    Calculates the weighted running average of the last sample in the series using the previous samples.
    """

    if len(series) != N:        # The expectation is that the series contains N samples

        raise RuntimeException

    if not weighing_function:           # No weighing function provided so we specify the default one

        weighing_function = lambda x: 1     # Standard mean over N values. NOTE: If you set N = 1 you get the exact value back

    sum = 0
    denom = 0

    for ii in range(N):

        sum += series[ii] * weighing_function(ii)
        denom += weighing_function(ii)

    return round( sum / float(denom), 2 )
