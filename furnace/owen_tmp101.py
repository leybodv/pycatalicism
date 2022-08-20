from pycatalicism.furnace.owen_protocol import OwenProtocol

class OwenTPM101():
    """
    """

    def __init__(self, device_name:str):
        """
        """
        self._connected = False
        self._owen_protocol = OwenProtocol()
        self._device_name = device_name
        self._logger = furnace_logging.get_logger(self.__class__.__name__)

    def connect(self):
        """
        """
        device_name = self._owen_protocol.request_string_parameter(parameter='dev')
        if self._device_name != device_name:
            raise FurnaceConnectionException('Cannot connect to furnace controller!')
        self._connected = True

    def set_temperature(self, temperature:float):
        """
        """
        if not self._connected:
            raise FurnaceStateException('Connect to furnace controller first!')
        self._owen_protocol.send_PIC_parameter(parameter='sp', value=temperature)

    def get_temperature(self) -> float:
        """
        """
        if not self._connected:
            raise FurnaceStateException('Connect to furnace controller first!')
        temperature = self._owen_protocol.request_PIC_parameter(parameter='sp')
        return temperature

    def set_temperature_control(self, value:bool):
        """
        """
        if not self._connected:
            raise FurnaceStateException('Connect to furnace controller first!')
        temperature_control = 1 if value else 0
        self._owen_protocol.send_unsigned_byte_parameter(parameter='r_s', value=temperature_control)
