# Author: Abid H. Mujtaba
# Date: 2014-04-13
#
# This module implements a client that communicates with the redis database used to store state.

import re
import redis


# Define the handle for the redis database
rds = redis.StrictRedis(host='localhost', port=6379, db=0)


def dump():
    """
    Method for printing a dump of redis keys and corresponding values
    """

    keys = rds.keys()
    keys.sort()

    for k in keys:

        print("{}: {}".format(k, rds.get(k)))


def change():
    """
    Method for listing and allowing the user to change ONE of the values in redis.
    """
    reActive = re.compile("^active_.*")

    keys = rds.keys()
    keys = [k for k in keys if not reActive.match(k)]
    keys.sort()

    for ii in range(len(keys)):                                             # Print keys with associated values indexed by an integer for choosing.
        print("{} - {}: {}".format(ii, keys[ii], rds.get(keys[ii])))

    jj = raw_input("\nIndex? ")

    if len(jj) == 0: return         # If an empty string (simply an ENTER has been pressed) it indicates no choice was made and so we exit

    jj = int(jj)

    v = raw_input("\n{} [{}]? ".format(keys[jj], rds.get(keys[jj])))

    if len(v) > 0:              # If an empty string (simply an ENTER has been pressed) is present it means keep the default value

        v = float(v)
        rds.set(keys[jj], v)


def toggle():
    """
    Method for listing and toggling the active flags of the decisions.
    """
    reActive = re.compile("^active_.*")

    keys = rds.keys()
    keys = [k for k in keys if reActive.match(k)]
    keys.sort()

    for ii in range(len(keys)):
        print("{} - {}: {}".format(ii, keys[ii], rds.get(keys[ii])))

    jj = raw_input("\nIndex? ")

    if len(jj) == 0: return

    jj = int(jj)
    v = rds.get(keys[jj]) == 'True'         # Convert the string to boolean by performing a comparison

    rds.set(keys[jj], not v)      # Flip/Toggle the specified value

    print("{} set to {}".format(keys[jj], not v))



def load():
    """
    Method for loading default values in to redis. Used if redis database is ever cleared.
    """

    rds.set(KEY_RISING_PEAK_ACTIVATION_THRESHOLD, 415)
    rds.set(KEY_RISING_PEAK_UPPER_LIMIT_FACTOR, 1.01)
    rds.set(KEY_RISING_PEAK_LOWER_LIMIT_FACTOR, 0.9925)
    rds.set(KEY_FALLING_TRENCH_ACTIVATION_THRESHOLD, 410)
    rds.set(KEY_FALLING_TRENCH_LOWER_LIMIT_FACTOR, 0.99)
    rds.set(KEY_FALLING_TRENCH_UPPER_LIMIT_FACTOR, 1.0075)
    rds.set(KEY_ABSOLUTE_ZERO_MINIMUM_THRESHOLD, 380)
    rds.set(KEY_MINIMIZE_LOSS_DROP_FACTOR, 0.97)
    rds.set(KEY_MIN_PROFIT_BAND_LOWER_FACTOR, 1.008)
    rds.set(KEY_MIN_PROFIT_BAND_UPPER_FACTOR, 1.02)
    rds.set(KEY_MIN_PROFIT_TRIGGER_THRESHOLD, 1.025)

    rds.set(KEY_ACTIVE_ABSOLUTE_ZERO, False)
    rds.set(KEY_ACTIVE_MINIMIZE_LOSS, False)
    rds.set(KEY_ACTIVE_MINIMUM_PROFIT, False)
    rds.set(KEY_ACTIVE_RISING_PEAK, False)
    rds.set(KEY_ACTIVE_FALLING_TRENCH, False)


# Activation keys and functions

KEY_ACTIVE_ABSOLUTE_ZERO = "active_absolute_zero"
def active_absolute_zero(): return rds.get(KEY_ACTIVE_ABSOLUTE_ZERO) == 'True'

KEY_ACTIVE_MINIMIZE_LOSS = "active_minimize_loss"
def active_minimize_loss(): return rds.get(KEY_ACTIVE_MINIMIZE_LOSS) == 'True'

KEY_ACTIVE_MINIMUM_PROFIT = "active_min_profit"
def active_minimum_profit(): return rds.get(KEY_ACTIVE_MINIMUM_PROFIT) == 'True'

KEY_ACTIVE_RISING_PEAK = "active_rising_peak"
def active_rising_peak(): return rds.get(KEY_ACTIVE_RISING_PEAK) == 'True'

KEY_ACTIVE_FALLING_TRENCH = "active_falling_trench"
def active_falling_trench(): return rds.get(KEY_ACTIVE_FALLING_TRENCH) == 'True'






# Define the key and function for accessing Rising Peak Activiation Threshold
KEY_RISING_PEAK_ACTIVATION_THRESHOLD = "rising_peak_activiation_threshold"
KEY_RISING_PEAK_UPPER_LIMIT_FACTOR = "rising_peak_upper_limit_factor"
KEY_RISING_PEAK_LOWER_LIMIT_FACTOR = "rising_peak_lower_limit_factor"

def rising_peak_activiation_threshold(): return float(rds.get(KEY_RISING_PEAK_ACTIVATION_THRESHOLD))

def rising_peak_upper_limit_factor():  return float(rds.get(KEY_RISING_PEAK_UPPER_LIMIT_FACTOR))

def rising_peak_lower_limit_factor():  return float(rds.get(KEY_RISING_PEAK_LOWER_LIMIT_FACTOR))



# Define the key and function for accessing Falling Trench Activation Threshold
KEY_FALLING_TRENCH_ACTIVATION_THRESHOLD = "falling_trench_activation_threshold"
KEY_FALLING_TRENCH_LOWER_LIMIT_FACTOR = "falling_trench_lower_limit_factor"
KEY_FALLING_TRENCH_UPPER_LIMIT_FACTOR = "falling_trench_upper_limit_factor"

def falling_trench_activation_threshold():  return float(rds.get(KEY_FALLING_TRENCH_ACTIVATION_THRESHOLD))

def falling_trench_lower_limit_factor():  return float(rds.get(KEY_FALLING_TRENCH_LOWER_LIMIT_FACTOR))

def falling_trench_upper_limit_factor():  return float(rds.get(KEY_FALLING_TRENCH_UPPER_LIMIT_FACTOR))



# Define the key and function for accessing Absolute Zero Activation Threshold
KEY_ABSOLUTE_ZERO_MINIMUM_THRESHOLD = "absolute_zero_min_threshold"

def absolute_zero_min_threshold():  return float(rds.get(KEY_ABSOLUTE_ZERO_MINIMUM_THRESHOLD))



# Define the key and function for accessing Minimum Loss Drop Factor
KEY_MINIMIZE_LOSS_DROP_FACTOR = "minimize_loss_drop_factor"


def minimize_loss_drop_factor():  return float(rds.get(KEY_MINIMIZE_LOSS_DROP_FACTOR))



# Define the keys and functions for accessing Minimum Profit values:
KEY_MIN_PROFIT_BAND_UPPER_FACTOR = "min_profit_band_upper_factor"
KEY_MIN_PROFIT_BAND_LOWER_FACTOR = "min_profit_band_lower_factor"
KEY_MIN_PROFIT_TRIGGER_THRESHOLD = "min_profit_trigger_threshold"

def min_profit_band_upper_factor(): return float(rds.get(KEY_MIN_PROFIT_BAND_UPPER_FACTOR))

def min_profit_band_lower_factor(): return float(rds.get(KEY_MIN_PROFIT_BAND_LOWER_FACTOR))

def min_profit_trigger_threshold(): return float(rds.get(KEY_MIN_PROFIT_TRIGGER_THRESHOLD))
