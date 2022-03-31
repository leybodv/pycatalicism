from pathlib import Path

from .conversion import Conversion
from .selectivity import Selectivity

class Exporter():
    """
    Abstract class
    """

    def export(self, output_data_path:Path, conversion:Conversion, selectivity:Selectivity|None):
        """
        """
        raise NotImplementedError()
