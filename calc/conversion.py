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
        for temperature, alpha in zip(self.temperatures, self.alphas):
            string = string + f'{temperature}\t{alpha}\n'
        return string
