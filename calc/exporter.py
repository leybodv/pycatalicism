from pathlib import Path

from pycatalicism.calc.conversion import Conversion
from pycatalicism.calc.selectivity import Selectivity

class Exporter():
    """
    Abstract class
    """

    def export(self, output_data_path:Path, conversion:Conversion, selectivity:Selectivity|None):
        """
        """
        raise NotImplementedError()
