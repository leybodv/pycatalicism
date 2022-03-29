class RawData():
    """
    Wrapper for imported data storage
    """

    def __init__(self, temperatures:list[float], initial_ambient_temperature:float|None=None):
        """
        """
        self.temperatures = temperatures
        self.init_amb_temp = initial_ambient_temperature
        raise NotImplementedError()

    def get_temperatures(self) -> list[float]:
        """
        """
        return self.temperatures

    def get_init_amb_temp(self) -> float|None:
        """
        """
        return self.init_amb_temp
