class RawData():
    """
    Wrapper for imported data storage
    """

    def __init__(self, temperatures:list[float], initial_ambient_temperature:float|None=None, initial_ambient_pressure:float|None=None):
        """
        """
        self.temperatures = temperatures
        self.init_amb_temp = initial_ambient_temperature
        self.init_amb_pres = initial_ambient_pressure
        raise NotImplementedError()

    def get_temperatures(self) -> list[float]:
        """
        """
        return self.temperatures

    def get_init_amb_temp(self) -> float|None:
        """
        """
        return self.init_amb_temp

    def get_init_amb_pres(self) -> float|None:
        """
        """
        return self.init_amb_pres
