#! /usr/bin/python

# This script reads prices from "prices.txt" and then creates plots of the prices, short and long moving averages and the difference between them. This will allow us to make judgements about buying and selling.


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from weighted_average import weighted_running_average


if __name__ == '__main__':

    fin = open("prices.txt")

    prices = []

    for line in fin.readlines(): prices.append(float(line.strip()))

    series = pd.Series(prices)

    sma = weighted_running_average(series, 10)
    lma = weighted_running_average(series, 25)

    sma = pd.Series(sma)
    lma = pd.Series(lma)

    delta = sma - lma
    index = list(range(len(delta)))

    plt.figure(1)

    gs = gridspec.GridSpec(2,1, height_ratios=[4,1])

    plt.subplot(gs[0])
    plt.plot(series, 'b')
    plt.plot(series, 'b.')
    plt.plot(sma, 'r')
    plt.plot(lma, 'k')
    plt.grid()

    plt.subplot(gs[1])
    plt.bar(index, delta)
    plt.grid()

    plt.show()