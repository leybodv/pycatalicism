from abc import ABC, abstractmethod

from pycatalicism.furnace.furnace_data import FurnaceData
from pycatalicism.furnace.furnace_exception import FurnaceException

class Controller(ABC):
    """
    """

    def __init__(self, port:str, baudrate:int, bytesize:int, parity:str, stopbits:float, timeout:float, write_timeout:float):
        """
        """
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.write_timeout = write_timeout
        if not self._handshake():
            raise FurnaceException('Cannot connect to furnace controller')

    @abstractmethod
    def heat(self, temperature:int, wait:int|None) -> FurnaceData:
        """
        """
        pass

    @abstractmethod
    def _handshake(self) -> bool:
        """
        """
        pass
