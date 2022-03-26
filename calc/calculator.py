import rawdata.RawData as RawData
import conversion.Conversion as Conversion
import selectivity.Selectivity as Selectivity
import activity.Activity as Activity

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
