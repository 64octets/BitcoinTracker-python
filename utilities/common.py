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
# Date: 2014-03-29
#
# Collection of functions which are common to a number of utilities.


from datetime import datetime
from dateutil.parser import parse
import pytz


def unix_timestamp(timestring):
    """
    Takes a timestring denoting the timestamp in UTC and converts it to the unix epoch.
    """

    dt = pytz.utc.localize( parse(timestring) )          # Parses the time-string and explicitly sets its locale to UTC

    epoch = pytz.utc.localize( datetime.utcfromtimestamp(0) )       # Get a localized datetime object corresponding to the start of the epoch
    delta = dt - epoch          # Calculate time difference between beginning of epoch and timestamp

    return int(delta.total_seconds())           # Converts delta to seconds which is the definition of the unix timestamp (seconds since epoch)
