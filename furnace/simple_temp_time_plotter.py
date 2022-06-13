from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.axes

from pycatalicism.furnace.plotter import Plotter
from pycatalicism.furnace.furnace_data import FurnaceData
import pycatalicism.furnace.furnace_logging as logging

class SimpleTempTimePlotter(Plotter):
    """
    Class for plotting temperature vs. time data.
    """

    def __init__(self):
        """
        Registers logger
        """
        self.logger = logging.get_logger(self.__class__.__name__)

    def plot(self, data:FurnaceData):
        """
        Plots temperature vs. time data in a separate window.
        NB: this will block main thread!

        parameters
        ----------
        data:FurnaceData
            Wrapper of temperature vs. time data
        """
        self.logger.info('Plotting temperature vs. time data')
        fig, ax = plt.subplots()
        ax = self._get_ax(data, ax)
        plt.show(block=True)

    def export_plot(self, data:FurnaceData, path:Path, fig_dpi:float, fig_height:float, fig_width:float):
        """
        Saves temperature vs. time plot.

        parameters
        ----------
        data:FurnaceData
            Wrapper of temperature vs. time data
        path:Path
            Path to save plot
        fig_dpi:float
            Figure dpi in dots per inch
        fig_height:float
            Figure height in inches
        fig_width:float
            Figure width in inches
        """
        self.logger.info(f'Exporting temperature vs. time plot to {path}')
        fig, ax = plt.subplots()
        ax = self._get_ax(data, ax)
        fig.set_dpi(fig_dpi)
        fig.set_figheight(fig_height)
        fig.set_figwidth(fig_width)
        fig.set_tight_layout(True)
        fig.savefig(fname=path)

    def _get_ax(self, data:FurnaceData, ax:matplotlib.axes.Axes) -> matplotlib.axes.Axes:
        """
        Constructs matplotlib.axes.Axes with temperature vs. time plot.

        parameters
        ----------
        data:FurnaceData
            Wrapper of temperature vs. time data
        ax:matplotlib.axes.Axes
            Axes to plot data to

        returns
        -------
        ax:matplotlib.axes.Axes
            Axes with plotted data
        """
        x = data.get_times()
        y = data.get_temperatures()
        ax.plot(x, y)
        ax.set_xlabel('Time, min')
        ax.set_ylabel('Temperature, °C')
        return ax
