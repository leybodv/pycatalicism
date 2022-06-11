from abc import ABC, abstractmethod
from pathlib import Path

from pycatalicism.furnace.furnace_data import FurnaceData

class Plotter(ABC):
    """
    Abstract class for plotting of time-temperature data received from furnace controller device. Subclasses must implement plot and export_plot methods.
    """

    @abstractmethod
    def plot(self, data:FurnaceData):
        """
        Plot time-temperature data.

        parameters
        ----------
        data:FurnaceData
            Wrapper containing lists of times and measured temperatures
        """
        pass

    @abstractmethod
    def export_plot(self, data:FurnaceData, path:Path, fig_dpi:float, fig_height:float, fig_width:float):
        """
        Exports plot to the specified path.

        parameters
        ----------
        data:FurnaceData
            Wrapper containing lists of times and measured temperatures
        path:Path
            Path to file to save exported plot
        fig_dpi:float
            Resolution of figure to use during export
        fig_height:float
            Figure height in pixels
        fig_width:float
            Figure width in pixels
        """
        pass
