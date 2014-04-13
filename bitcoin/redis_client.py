# Author: Abid H. Mujtaba
# Date: 2014-04-13
#
# This module implements a client that communicates with the redis database used to store state.

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


def load():
    """
    Method for loading default values in to redis. Used if redis database is ever cleared.
    """

    rds.set(KEY_RISING_PEAK_ACTIVATION_THRESHOLD, 415)
    rds.set(KEY_RISING_PEAK_UPPER_LIMIT_FACTOR, 1.01)
    rds.set(KEY_FALLING_TRENCH_ACTIVATION_THRESHOLD, 410)
    rds.set(KEY_FALLING_TRENCH_LOWER_LIMIT_FACTOR, 0.99)
    rds.set(KEY_ABSOLUTE_ZERO_MINIMUM_THRESHOLD, 380)
    rds.set(KEY_MINIMIZE_LOSS_DROP_FACTOR, 0.97)
    rds.set(KEY_MIN_PROFIT_BAND_LOWER_FACTOR, 1.008)
    rds.set(KEY_MIN_PROFIT_BAND_UPPER_FACTOR, 1.02)
    rds.set(KEY_MIN_PROFIT_TRIGGER_THRESHOLD, 1.025)



# Define the key and function for accessing Rising Peak Activiation Threshold
KEY_RISING_PEAK_ACTIVATION_THRESHOLD = "rising_peak_activiation_threshold"
KEY_RISING_PEAK_UPPER_LIMIT_FACTOR = "rising_peak_upper_limit_factor"

def rising_peak_activiation_threshold(): return int(rds.get(KEY_RISING_PEAK_ACTIVATION_THRESHOLD))

def rising_peak_upper_limit_factor():  return float(rds.get(KEY_RISING_PEAK_UPPER_LIMIT_FACTOR))



# Define the key and function for accessing Falling Trench Activation Threshold
KEY_FALLING_TRENCH_ACTIVATION_THRESHOLD = "falling_trench_activation_threshold"
KEY_FALLING_TRENCH_LOWER_LIMIT_FACTOR = "falling_trench_lower_limit_factor"

def falling_trench_activation_threshold():

    return int(rds.get(KEY_FALLING_TRENCH_ACTIVATION_THRESHOLD))

def falling_trench_lower_limit_factor():  return float(rds.get(KEY_FALLING_TRENCH_LOWER_LIMIT_FACTOR))



# Define the key and function for accessing Absolute Zero Activation Threshold
KEY_ABSOLUTE_ZERO_MINIMUM_THRESHOLD = "absolute_zero_min_threshold"

def absolute_zero_min_threshold():  return int(rds.get(KEY_ABSOLUTE_ZERO_MINIMUM_THRESHOLD))



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