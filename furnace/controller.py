from abc import ABC, abstractmethod

from pycatalicism.furnace.furnace_data import FurnaceData

class Controller(ABC):
    """
    """

    @abstractmethod
    def heat(self, temperature:int, wait:int|None) -> FurnaceData:
        """
        """
        pass
