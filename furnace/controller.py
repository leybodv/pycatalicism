from abc import ABC, abstractmethod

from pycatalicism.furnace.furnace_data import FurnaceData
from pycatalicism.furnace.furnace_exception import FurnaceException

class Controller(ABC):
    """
    Abstract class representing furnace PID controller. Subclasses must implement heat and _handshake methods.
    """

    def __init__(self, port:str, baudrate:int, bytesize:int, parity:str, stopbits:float, timeout:float, write_timeout:float, rtscts:bool):
        """
        Assigns parameters to instance variables and performs handshake with physical furnace controller.

        parameters
        ----------
        port:str
            COMM port through which connection with controller is made
        baudrate:int
            Data exchange rate, must match the one at the controller device
        bytesize:int
            Size of byte of information to be sent to the controller
        parity:str
            Whether to control parity
        stopbits:float
            How many stopbits to use when sending information to the device
        timeout:float
            Read timeout in seconds. See pyserial documentation for details (https://pyserial.readthedocs.io/en/latest/pyserial_api.html)
        write_timeout:float
            Write timeout in seconds. See pyserial documentation for details (https://pyserial.readthedocs.io/en/latest/pyserial_api.html)
        rtscts:bool
            Enable hardware flow control. See pyserial documentation for details (https://pyserial.readthedocs.io/en/latest/pyserial_api.html)

        raises
        ------
        FurnaceException
            if handshake with device was unsuccessful
        """
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.write_timeout = write_timeout
        self.rtscts = rtscts
        if not self._handshake():
            raise FurnaceException('Cannot connect to furnace controller')

    @abstractmethod
    def heat(self, temperature:int, wait:int|None) -> FurnaceData:
        """
        Heat furnace to specified temperature and wait for specified time in minutes if wait is not None

        parameters
        ----------
        temperature:int
            Temperature in °C
        wait:int or None
            If None, heat furnace to specified temperature and return, wait for specified time in minutes, turn off heating and return

        returns
        -------
        furnace_data:FurnaceData
            Wrapper with time-temperature data
        """
        pass

    @abstractmethod
    def _handshake(self) -> bool:
        """
        Method to check proper connection with device

        returns
        -------
        True if connection was succsessful
        """
        pass
