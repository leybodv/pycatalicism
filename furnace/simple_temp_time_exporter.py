from pathlib import Path

from pycatalicism.furnace.exporter import Exporter
from pycatalicism.furnace.furnace_data import FurnaceData

class SimpleTempTimeExporter(Exporter):
    """
    Class for exporting temperature vs. time data in a simple format defined in __str__ method of FurnaceData class.
    """

    def export_data(self, data:FurnaceData, path:Path):
        """
        Exports temperature vs. time data in a format defined in __str__ method of FurnaceData class into file at path.

        parameters
        ----------
        data:FurnaceData
            Wrapper of temperature vs. time data
        path:Path
            Path to file to export data to.
        """
        with path.open(mode='w') as f:
            f.write(str(data))
