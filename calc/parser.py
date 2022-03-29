from pathlib import Path

from .rawdata import RawData

class Parser():
    """
    Abstract class
    """

    def parse_data(self, input_data_path:Path) -> RawData:
        """
        """
        raise NotImplementedError()
