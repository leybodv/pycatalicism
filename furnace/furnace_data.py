class FurnaceData():
    """
    """

    def __init__(self, times:list[float], temperatures:list[float]):
        """
        """
        self.times = times
        self.temperatures = temperatures

    def get_times(self) -> list[float]:
        """
        """
        return self.times

    def get_temperatures(self) -> list[float]:
        """
        """
        return self.temperatures
