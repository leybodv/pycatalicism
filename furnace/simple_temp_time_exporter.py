from pathlib import Path

from pycatalicism.furnace.exporter import Exporter
from pycatalicism.furnace.furnace_data import FurnaceData
import pycatalicism.furnace.furnace_logging as logging

class SimpleTempTimeExporter(Exporter):
    """
    Class for exporting temperature vs. time data in a simple format defined in __str__ method of FurnaceData class.
    """

    def __init__(self):
        """
        Registers logger with the class
        """
        self.logger = logging.get_logger(self.__class__.__name__)

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
        self.logger.info(f'Exporting data to {path}')
        with path.open(mode='w') as f:
            f.write(str(data))
