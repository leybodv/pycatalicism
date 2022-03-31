from .calculator import Calculator
from .rawdata import RawData
from .conversion import Conversion
from .selectivity import Selectivity

class CO2HydrogenationCalculator(Calculator):
    """
    """

    def __init__(self):
        """
        """
        raise NotImplementedError()

    def calculate_conversion(self, input_data:RawData) -> Conversion:
        """
        """
        raise NotImplementedError()

    def calculate_selectivity(self, input_data:RawData) -> Selectivity:
        """
        """
        raise NotImplementedError()
