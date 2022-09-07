import numpy as np

class Conversion():
    """
    Wrapper for conversion data storage. Conversion is stored as two parallel numpy.ndarrays of floats: temperature and conversion data.
    """

    def __init__(self, temperatures:list[float], alphas:list[float], sample_name:str|None):
        """
        Assign parameters to instance variables after conversion lists to numpy.ndarrays.

        parameters
        ----------
        temperatures:list[float]
            list of temperatures
        alphas:list[float]
            list of conversions
        sample_name:str|None
        """
        self.temperatures = np.array(temperatures)
        self.alphas = np.array(alphas)
        self.sample_name = sample_name

    def __str__(self) -> str:
        """
        Get string representation of covnersion vs. temperature data in a format:

        Sample<tab><sample-name><br>
        <br>
        Temperature<tab>Conversion<br>
        <temperature><tab><covnersion><br>
        ...

        returns
        -------
        string:str
            string representation of conversion vs. temperature data
        """
        string = f'Sample\t{self.sample_name}\n\nTemperature\tConversion\n'
        sorted_conversion = self.get_sorted()
        for temperature, alpha in zip(sorted_conversion.get_temperatures(), sorted_conversion.get_alphas()):
            string = string + f'{temperature}\t{alpha}\n'
        return string

    def get_sorted(self) -> 'Conversion':
        """
        Get conversion data sorted by temperature from lower to higher value

        returns
        -------
        conversion:Conversion
            wrapper of sorted conversion data
        """
        zipped_lists = zip(self.temperatures, self.alphas, strict=True)
        sorted_pairs = sorted(zipped_lists)
        tuples = zip(*sorted_pairs)
        sorted_temperatures, sorted_alphas = [list(tuple) for tuple in tuples]
        return Conversion(sorted_temperatures, sorted_alphas, self.sample_name)

    def get_temperatures(self) -> np.ndarray[float, np.dtype]:
        """
        Get temperatures as numpy.ndarray list

        returns
        -------
        temperatures:ndarray
            temperatures stored in this wrapper
        """
        return self.temperatures

    def get_alphas(self) -> np.ndarray[float, np.dtype]:
        """
        Get conversions as numpy.ndarray list

        returns
        -------
        conversions:ndarray
            conversions stored in this wrapper
        """
        return self.alphas
