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
# Date: 2014-03-01
#
# This script reads bitcoin data from "data.txt" and then displays it in an interactive plot to aid in analysis.
#
# Furthermore it calculates a weighted moving average to smooth out the fluctuations and grant greater insight in to how
# the price is trending.

from chaco.api import ArrayPlotData, Plot
from chaco.tools.api import PanTool, ZoomTool
import datetime
from enable.component_editor import ComponentEditor
import numpy
import re
from traits.api import HasTraits, Instance
from traitsui.api import Item, View

# Define colors to be used by the  plots
RED = (0.9, 0, 0)
LIGHT_RED = (0.9, 0, 0, 0.8)

GREEN = (0, 0.9, 0)
LIGHT_GREEN = (0, 0.9, 0, 0.7)


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

        self.t = t
        self.b = b
        self.s = s

        plot_data = ArrayPlotData(t=t, b=b, s=s, wb=wb, ws=ws)

        plot = Plot(plot_data)
        self.plot = plot

        # Calculate range of plot so it shows latest 1 day of data
        end = t[-1]
        start = end - 86400

        self._configure_plot(plot, start, end)

        # Scatter point for prices
        buy_renderer = plot.plot(("t", "b"), type="scatter", color=RED)[0]
        sell_renderer = plot.plot(("t", "s"), type="scatter", color=GREEN)[0]

        # Line plot to connect the scatter points together
        plot.plot(("t", "b"), type="line", color=LIGHT_RED)        # Using RGBA color tuple to get a lighter color
        plot.plot(("t", "s"), type="line", color=LIGHT_GREEN)

        # Line plot of moving average of prices (thicker to indicate this fact)
        plot.plot(("t", "wb"), type="line", color=RED, line_width=2)
        plot.plot(("t", "ws"), type="line", color=GREEN, line_width=2)

        buy_renderer.marker_size = 3
        buy_renderer.marker = "circle"

        sell_renderer.marker_size = 3
        sell_renderer.marker = "circle"

        plot.title = "Current Price - Buy: ${} - Sell: ${}".format(buy[-1], sell[-1])       # Display current price in title


    def _configure_plot(self, plot, start, end):
        """
        Configures the appearance of the plot
        """

        plot.bgcolor = "black"
        plot.title_color = "white"

        plot.y_axis.orientation = "right"
        plot.y_axis.tick_color = "white"
        plot.y_axis.tick_label_color = "white"

        plot.x_axis.tick_color = "white"
        plot.x_axis.tick_label_color = "white"

        plot.x_grid.line_weight = 0         # Remove x Grid lines

        pan = PanTool(component=plot)       # Set up PanTool so that it is constrained to move along the x-direction only
        pan.constrain = True
        pan.constrain_direction = 'x'
        plot.tools.append(pan)        # Add Pan and Zoom abilities to the plot

        zoom = ZoomTool(component=plot, tool_mode="range", axis="index", always_on=False)       # We create the ZoomTool to zoom along the x-axis only
        plot.tools.append(zoom)

        plot.x_axis.tick_label_formatter = lambda tick: self._format_time(tick)      # Set formatter for time axis tick labels

        plot.index_mapper.range.set_bounds(start, end)         # Set range of index (x values i.e. domain)

        plot.index_mapper.range.on_trait_change(self._xrange_changed, name='_low_value')        # We attach a listener on the range that is called when the _low_value attribute is changed
        self._xrange_changed()      # We call this initially to fit the y-range initially


    def _y_bounds(self):
        """
        Calculates the min and max values of the arrays b and s in the x-range currently chosen
        """

        (a, b) = self.plot.index_mapper.range.bound_data(self.t)        # We find the indices that bound the data self.t in the currently chosen x_range

        min = 1e6       # Start with a maximum possible value from which to go down
        max = 0

        for jj in range(a, b):      # We iterate over the indices of the bounds finding the min and max values of self.b and self.s in the range

            if self.b[jj] < min:
                min = self.b[jj]

            if self.s[jj] < min:
                min = self.s[jj]

            if self.b[jj] > max:
                max = self.b[jj]

            if self.s[jj] > max:
                max = self.b[jj]

        return min, max


    def _xrange_changed(self):
        """
        Method called when the xrange is changed so that the yrange can be changed to better fit the y-values
        """
        # Calculate the highest and lowest value of the graphs in the specified x-range.
        (y_min, y_max) = self._y_bounds()
        delta = 0.1 * (y_max - y_min)       # We calculate margins on the bound using 10% of the data-spread

        self.plot.value_mapper.range.set_bounds(y_min - delta, y_max + delta)


    def _format_time(self, time):
        """
        Method for taking the Unix timestamp in the time-series domain and converting it in to a human-readable format
        """
        return datetime.datetime.fromtimestamp(time).strftime("%m-%d %H:%M")



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

    # Define the weighted sum sampling window to be 1 hours: i.e. the number of 5 min intervals in 1 hours
    N = 1 * 12

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