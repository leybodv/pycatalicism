from pycatalicism.calc.rawdata import RawData
from pycatalicism.calc.conversion import Conversion
from pycatalicism.calc.selectivity import Selectivity
from pycatalicism.calc.activity import Activity

class Calculator():
    """
    Abstract class
    """

    def calculate_conversion(self, input_data:RawData) -> Conversion:
        """
        """
        raise NotImplementedError()

    def calculate_selectivity(self, input_data:RawData) -> Selectivity:
        """
        """
        raise NotImplementedError()

    def calculate_activity(self, input_data:RawData) -> Activity:
        """
        """
        raise NotImplementedError()
