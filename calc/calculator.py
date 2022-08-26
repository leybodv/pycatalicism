from calc.rawdata import RawData
from calc.conversion import Conversion
from calc.selectivity import Selectivity
from calc.activity import Activity

class Calculator():
    """
    Abstract class to calculate catalyst's activity, selectivity or conversion for different reactions of interest. Concrete classes should override corresponding abstract methods of this class.
    """

    def calculate_conversion(self, input_data:RawData) -> Conversion:
        """
        Calculate conversion vs. temperature data. Abstract method, should be overriden by concrete classes.

        parameters
        ----------
        input_data:RawData
            input data for calculation containing concentrations of reaction participants at different temperatures

        returns
        -------
        conversion:Conversion
            Wrapper of conversion vs. temperature data

        raises
        ------
        exception:NotImplementedError
            if this method is not overriden but is used
        """
        raise NotImplementedError()

    def calculate_selectivity(self, input_data:RawData) -> Selectivity:
        """
        Calculate selectivity vs. temperature data. Abstract method, should be overriden by concrete classes.

        parameters
        ----------
        input_data:RawData
            input data for calculation, containing concentrations of reaction participants at different temperatures

        returns
        -------
        selectivity:Selectivity
            Wrapper of selectivity vs. temperature data

        raises
        ------
        exception:NotImplementedError
            if this method is not overriden but is used
        """
        raise NotImplementedError()

    def calculate_activity(self, input_data:RawData) -> Activity:
        """
        Calculate activity vs. temperature data. Abstract method, should be overriden by concrete classes.

        parameters
        ----------
        input_data:RawData
            input data for calculation, containing concentrations of reaction participants at different temperatures

        returns
        -------
        activity:Activity
            Wrapper of activity vs. temperature data

        raises
        ------
        exception:NotImplementedError
            if this method is not overriden but is used
        """
        raise NotImplementedError()
