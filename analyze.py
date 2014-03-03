#! /usr/bin/python

# Author: Abid H. Mujtaba
# Date: 2014-03-01
#
# This script reads bitcoin data from "data.txt" and then displays it in an interactive plot to aid in analysis.
#
# Furthermore it calculates a weighted moving average to smooth out the fluctuations and grant greater insight in to how
# the price is trending.

from chaco.api import ArrayPlotData, Plot
from chaco.tools.api import PanTool, ZoomTool
from enable.component_editor import ComponentEditor
import math
import numpy
import re
from traits.api import HasTraits, Instance
from traitsui.api import Item, View


class PricePlot(HasTraits):

    plot = Instance(Plot)

    traits_view = View(
                        Item('plot', editor=ComponentEditor(), show_label=False),
                        width=1200, height=1000, resizable=True, title="Bitcoin Prices")


    def __init__(self, time, buy, sell, weighted_buy, weighted_sell):

        t = numpy.array(time)       # Convert lists to numpy arrays in preparation for plotting
        b = numpy.array(buy)
        s = numpy.array(sell)
        wb = numpy.array(weighted_buy)
        ws = numpy.array(weighted_sell)

        plot_data = ArrayPlotData(t=t, b=b, s=s, wb=wb, ws=ws)

        plot = Plot(plot_data)

        self._setup_plot(plot)

        buy_renderer = plot.plot(("t", "b"), type="scatter", color="red")[0]
        sell_renderer = plot.plot(("t", "s"), type="scatter", color="green")[0]

        plot.plot(("t", "wb"), type="line", color="red")
        plot.plot(("t", "ws"), type="line", color="green")

        buy_renderer.marker_size = 3
        buy_renderer.marker = "circle"

        sell_renderer.marker_size = 3
        sell_renderer.marker = "circle"

        self.plot = plot


    def _setup_plot(self, plot):
        """
        Configures the appearance of the plot
        """

        plot.bgcolor = "black"

        plot.y_axis.orientation = "right"
        plot.y_axis.tick_color = "white"
        plot.y_axis.tick_label_color = "white"

        plot.x_axis.tick_color = "white"
        plot.x_axis.tick_label_color = "white"

        plot.x_grid.line_weight = 0         # Remove x Grid lines

        plot.tools.append(PanTool(plot))        # Add Pan and Zoom abilities to the plot
        plot.tools.append(ZoomTool(plot))



def weighted_running_average(series, N, weighing_function = None):
    """
    Calculates the Weighted Running Average of a sequence over the last N values using the specified weighing_funciton.
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

        weighted_series.append(sum / float(denom))     # Append the calculated weighted sum to the output series

    return weighted_series



if __name__ == '__main__':

    # Define the weighted sum sampling window to be 3 hours: i.e. the number of 5 min intervals in 3 hours
    N = 3 * 12

    # Exponential weighing factor:          (The larger the factor the more effect old values have on the average)
    FACTOR = 1.0 / 1e3

    # Define the weighing function used to calculate the average
    weighing_function = lambda x: (N - x)           # We use a linear weighing function. x = 0 is the end-value
                                                    # and as x increases we are looking at successively older values


    # Read data from file
    fin = open("data.txt")

    # Define regular expression to extract information
    RegEx = re.compile("^(\d+) (\d+\.\d*) (\d+\.\d*)$")

    time = []
    buy = []
    sell = []

    for line in fin.readlines():

        m = RegEx.match(line.strip())

        if m:

            time.append(int(m.group(1)))
            buy.append(float(m.group(2)))
            sell.append(float(m.group(3)))

        else:

            print("RegEx error parsing data: " + line)

    weighted_buy = weighted_running_average(buy, N, weighing_function)
    weighted_sell = weighted_running_average(sell, N, weighing_function)


    PricePlot(time, buy, sell, weighted_buy, weighted_sell).configure_traits()