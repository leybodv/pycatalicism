from abc import ABC, abstractmethod
from pathlib import Path

from pycatalicism.furnace.furnace_data import FurnaceData

class Plotter(ABC):
    """
    """

    @abstractmethod
    def plot(self, data:FurnaceData):
        """
        """
        pass

    @abstractmethod
    def export_plot(self, data:FurnaceData, path:Path):
        """
        """
        pass
