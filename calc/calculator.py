class Calculator():
    """
    """

    def __init__(self, reaction:str):
        """
        """
        self.calculator = calculator_factory.get_calculator(reaction)

    def calculate_conversion(self, input_data:RawData):
        """
        """
        raise NotImplementedError()

    def calculate_selectivity(self, input_data):
        """
        """
        raise NotImplementedError()

    def calculate_activity(self, input_data):
        """
        """
        raise NotImplementedError()
