from pathlib import Path

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
        """
        raise NotImplementedError()

    def export_plot(self, path:Path):
        """
        """
        raise NotImplementedError()
