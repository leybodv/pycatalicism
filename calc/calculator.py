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
