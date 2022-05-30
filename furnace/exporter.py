from abc import ABC, abstractmethod
from pathlib import Path

from pycatalicism.furnace.furnace_data import FurnaceData

class Exporter(ABC):
    """
    """

    @abstractmethod
    def export_data(self, data:FurnaceData, path:Path):
        """
        """
        pass
