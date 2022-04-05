from pathlib import Path

from pycatalicism.calc.rawdata import RawData

class Parser():
    """
    Abstract class
    """

    def parse_data(self, input_data_path:Path, initial_data_path:Path) -> RawData:
        """
        """
        raise NotImplementedError()
