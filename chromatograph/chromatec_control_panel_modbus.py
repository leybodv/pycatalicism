from enum import Enum

from pymodbus.client.sync import ModbusTcpClient

import chromatograph_logging

class WorkingStatus(Enum):
    """
    """
    PURGING = 5
    ANALYSIS = 9
    PREPARATION = 1
    READY_FOR_ANALYSIS = 4

class ConnectionStatus(Enum):
    """
    """
    CP_ON_CONNECTED = 7
    CP_ON_NOT_CONNECTED = 1
    CP_OFF_NOT_CONNECTED = 0

class ChromatographCommand(Enum):
    """
    """
    START_ANALYSIS = 6

class ApplicationCommand(Enum):
    """
    """
    START_CONTROL_PANEL = 1

class ChromatecControlPanelModbus():
    """
    """

    def __init__(self, modbus_id:int, working_status_input_address:int, serial_number_input_address:int, connection_status_input_address:int, method_holding_address:int, chromatograph_command_holding_address:int, application_command_holding_address:int):
        """
        """
        self._modbus_id = modbus_id
        self._working_status_input_address = working_status_input_address
        self._serial_number_input_address = serial_number_input_address
        self._connection_status_input_address = connection_status_input_address
        self._method_holding_address = method_holding_address
        self._chromatograph_command_holding_address = chromatograph_command_holding_address
        self._application_command_holding_address = application_command_holding_address
        self._modbus_client = ModbusTcpClient()
        self._logger = chromatograph_logging.get_logger(self.__class__.__name__)

    def get_current_working_status(self) -> WorkingStatus:
        """
        """
        response = self._modbus_client.read_input_registers(address=self._working_status_input_address, count=2, unit=self._modbus_id)
        current_status_id = self._bytes_to_int(response.registers)
        current_status = WorkingStatus(current_status_id)
        return current_status

    def get_serial_number(self) -> str:
        """
        """
        response = self._modbus_client.read_input_registers(address=self._serial_number_input_address, count=15, unit=self._modbus_id)
        serial_number = self._bytes_to_string(response.registers)
        return serial_number

    def get_connection_status(self) -> ConnectionStatus:
        """
        """
        raise NotImplementedError()

    def set_instrument_method(self, method_id:int):
        """
        """
        self._modbus_client.write_registers(address=self._method_holding_address, values=[method_id], unit=self._modbus_id)

    def send_chromatograph_command(self, command:ChromatographCommand):
        """
        """
        self._modbus_client.write_registers(address=self._chromatograph_command_holding_address, values=[command.value], unit=self._modbus_id)

    def send_application_command(self, command:ApplicationCommand):
        """
        """
        raise NotImplementedError()

    def _bytes_to_int(self, response_bytes:list[int]) -> int:
        """
        Converts bytes received from chromatograph to integer.

        parameters
        ----------
        response_bytes:list[int]
            bytes received from chromatograph

        returns
        -------
        integer:int
            decoded integer
        """
        self._logger.debug(f'Converting bytes: {response_bytes} to int')
        integer = response_bytes[0]
        self._logger.log(5, f'{integer = }')
        return integer

    def _bytes_to_string(self, response_bytes:list[int]) -> str:
        """
        Converts bytes received from chromatograph to string.

        parameters
        ----------
        response_bytes:list[int]
            bytes received from chromatograph

        returns
        -------
        string:str
            decoded string
        """
        self._logger.debug(f'Converting bytes: {response_bytes} to string')
        string = b''
        for b in response_bytes:
            string += b.to_bytes(2, 'big')
        self._logger.log(5, f'String bytes: {string = }')
        string = string.decode().rstrip('\x00')
        self._logger.log(5, f'{string = }')
        return string
