class RawData():
    """
    Wrapper for imported data storage
    """

    def __init__(self, temperatures:list[float]):
        """
        """
        self.temperatures = temperatures
        raise NotImplementedError()

    def get_temperatures(self) -> list[float]:
        """
        """
        return self.temperatures
