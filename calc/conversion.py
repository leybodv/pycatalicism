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
