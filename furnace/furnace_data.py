class FurnaceData():
    """
    Wrapper class representing time-temperature dependence data
    """

    def __init__(self, times:list[float], temperatures:list[float]):
        """
        Assigns parameters to instance variables.

        parameters
        ----------
        times:list[float]
            list of times in minutes during furnace heating and isothermal step
        temperatures:list[float]
            list of temperatures in °C during furnace heating and isothermal step
        """
        self.times = times
        self.temperatures = temperatures

    def __str__(self) -> str:
        """
        Make string representation of the object. Format of data is:
            Time, min<tab>Temperature, °C<LF>
            <time><tab><temperature><LF>
            ...

        returns
        -------
        string:str
            String representation of the object
        """
        string = 'Time, min\tTemperature, °C\n'
        for time, temperature in zip(self.times, self.temperatures):
            string = string + f'{time}\t{temperature}\n'
        return string

    def get_times(self) -> list[float]:
        """
        Get times list wrapped by object

        returns
        -------
        times:list[float]
            list of times in minutes during furnace heating and isothermal step
        """
        return self.times

    def get_temperatures(self) -> list[float]:
        """
        Get temperatures list wrapped by object

        returns
        -------
        temperatures:list[float]
            list of temperatures in °C during furnace heating and isothermal step
        """
        return self.temperatures
