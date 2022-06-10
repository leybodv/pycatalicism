from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.axes

from pycatalicism.furnace.plotter import Plotter
from pycatalicism.furnace.furnace_data import FurnaceData

class SimpleTempTimePlotter(Plotter):
    """
    """

    def __init__(self):
        """
        """
        raise NotImplementedError()

    def plot(self, data:FurnaceData):
        """
        NB: this will block main thread!
        """
        fig, ax = plt.subplots()
        ax = self._get_ax(data, ax)
        plt.show(block=True)

    def export_plot(self, path:Path):
        """
        """
        raise NotImplementedError()

    def _get_ax(self, data:FurnaceData, ax:matplotlib.axes.Axes) -> matplotlib.axes.Axes:
        """
        """
        x = data.get_times()
        y = data.get_temperatures()
        ax.plot(x, y)
        ax.set_xlabel('Time, min')
        ax.set_ylabel('Temperature, °C')
        return ax
