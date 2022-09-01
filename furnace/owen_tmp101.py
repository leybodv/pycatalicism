import pycatalicism.furnace.furnace_logging as furnace_logging
from pycatalicism.furnace.owen_protocol import OwenProtocol
from pycatalicism.furnace.furnace_exceptions import FurnaceConnectionException, FurnaceStateException

class OwenTPM101():
    """
    Class represents simplified version of Owen TPM101 temperature controller. Far less parameters can be used in this class in comparison to the real controller.
    """

    def __init__(self, device_name:str, owen_protocol:OwenProtocol):
        """
        Assign parameters to instance variables, initialize connection flag and register logger.

        parameters
        ----------
        device_name:str
            The name of the controller which is returned via serial protocol.
        owen_protocol:OwenProtocol
            Protocol used for communication over serial port.
        """
        self._connected = False
        self._owen_protocol = owen_protocol
        self._device_name = device_name
        self._logger = furnace_logging.get_logger(self.__class__.__name__)

    def connect(self):
        """
        Connect to the device. Check if device name returned by the controller is the same as one provided at the initialization. This method must be run before any other method of this class.

        raises
        ------
        FurnaceConnectionException
            if device_name does not match
        """
        self._logger.info('Connecting to temperature controller.')
        device_name = self._owen_protocol.request_string(parameter='dev')
        if self._device_name != device_name:
            raise FurnaceConnectionException('Cannot connect to furnace controller!')
        self._connected = True

    def set_temperature(self, temperature:float):
        """
        Set temperature to the specified value.

        parameters
        ----------
        temperature:float
            temperature in °C

        raises
        ------
        FurnaceStateException
            if connect method was not called
        """
        if not self._connected:
            raise FurnaceStateException('Connect to furnace controller first!')
        self._logger.info(f'Setting temperature to {temperature}°C')
        self._owen_protocol.send_PIC(parameter='sp', value=temperature)

    def get_temperature(self) -> float:
        """
        Get temperature from the controller

        returns
        -------
        temperature:float
            temperature in °C

        raises
        ------
        FurnaceStateException
            if connect method was not called
        """
        if not self._connected:
            raise FurnaceStateException('Connect to furnace controller first!')
        self._logger.info('Requesting temperature from furnace controller.')
        temperature = self._owen_protocol.request_PIC(parameter='pv')
        self._logger.debug(f'{temperature = }')
        return temperature

    def set_temperature_control(self, value:bool):
        """
        Turn temperature control ON or OFF.

        parameters
        ----------
        value:bool
            True to turn temperature control ON

        raises
        ------
        FurnaceStateException
            if connect method was not called
        """
        if not self._connected:
            raise FurnaceStateException('Connect to furnace controller first!')
        self._logger.info(f'Setting temperature control to {value}')
        temperature_control = 1 if value else 0
        self._owen_protocol.send_unsigned_byte(parameter='r-s', value=temperature_control)
