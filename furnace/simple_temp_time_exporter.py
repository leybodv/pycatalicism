from pathlib import Path

from pycatalicism.furnace.exporter import Exporter
from pycatalicism.furnace.furnace_data import FurnaceData

class SimpleTempTimeExporter(Exporter):
    """
    """

    def export_data(self, data:FurnaceData, path:Path):
        """
        """
        raise NotImplementedError()
