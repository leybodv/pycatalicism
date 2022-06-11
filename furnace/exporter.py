from abc import ABC, abstractmethod
from pathlib import Path

from pycatalicism.furnace.furnace_data import FurnaceData

class Exporter(ABC):
    """
    Abstract class representing objects responsible for export of time-temperature data. Concrete subclasses must implement export_data method.
    """

    @abstractmethod
    def export_data(self, data:FurnaceData, path:Path):
        """
        Export data to path provided as parameter to method. Format of exported data is defined by concrete implementation.

        parameters
        ----------
        data:FurnaceData
            Wrapper of time-temperature data
        path:Path
            Path to file to export data to
        """
        pass
