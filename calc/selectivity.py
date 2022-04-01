class Selectivity():
    """
    Wrapper for selectivity data storage
    """

    def __init__(self, temperatures:list[float], selectivities:list[dict[str,float]]):
        """
        """
        self.temperatures = temperatures
        self.selectivities = selectivities
