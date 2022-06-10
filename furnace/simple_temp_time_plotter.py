from pathlib import Path

import matplotlib.pyplot as plt

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
        x = data.get_times()
        y = data.get_temperatures()
        ax.plot(x, y)
        ax.set_xlabel('Time, min')
        ax.set_ylabel('Temperature, °C')
        plt.show(block=True)

    def export_plot(self, path:Path):
        """
        """
        raise NotImplementedError()
