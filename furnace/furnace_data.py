class FurnaceData():
    """
    """

    def __init__(self, times:list[float], temperatures:list[float]):
        """
        """
        self.times = times
        self.temperatures = temperatures

    def __str__(self) -> str:
        """
        """
        string = 'Time, min\tTemperature, °C\n'
        for time, temperature in zip(self.times, self.temperatures):
            string = string + f'{time}\t{temperature}\n'
        return string

    def get_times(self) -> list[float]:
        """
        """
        return self.times

    def get_temperatures(self) -> list[float]:
        """
        """
        return self.temperatures
