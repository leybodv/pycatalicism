from pathlib import Path
import rawdata.RawData as RawData

class Parser():
    """
    Abstract class
    """

    def parse_data(self, input_data_path:Path) -> RawData:
        """
        """
        raise NotImplementedError()
