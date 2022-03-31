import numpy as np

class Conversion():
    """
    Wrapper for conversion data storage
    """

    def __init__(self, temperatures:list[float], alphas:list[float]):
        """
        """
        self.temperatures = np.array(temperatures)
        self.alphas = np.array(alphas)

    def __str__(self) -> str:
        """
        """
        string = 'Temperature\tConversion\n'
        sorted_conversion = self.get_sorted()
        for temperature, alpha in zip(sorted_conversion.get_temperatures(), sorted_conversion.get_alphas()):
            string = string + f'{temperature}\t{alpha}\n'
        return string

    def get_sorted(self) -> 'Conversion':
        """
        """
        zipped_lists = zip(self.temperatures, self.alphas, strict=True)
        sorted_pairs = sorted(zipped_lists)
        tuples = zip(*sorted_pairs)
        sorted_temperatures, sorted_alphas = [list(tuple) for tuple in tuples]
        return Conversion(sorted_temperatures, sorted_alphas)

    def get_temperatures(self) -> np.ndarray[float, np.dtype]:
        """
        """
        return self.temperatures

    def get_alphas(self) -> np.ndarray[float, np.dtype]:
        """
        """
        return self.alphas
