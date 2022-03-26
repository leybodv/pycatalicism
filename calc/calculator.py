class Calculator():
    """
    """

    def __init__(self, reaction:str):
        """
        """
        self.calculator = calculator_factory.get_calculator(reaction)

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
