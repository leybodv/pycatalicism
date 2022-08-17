from enum import Enum

from pymodbus.client.sync import ModbusTcpClient

import pycatalicism.chromatograph.chromatograph_logging as chromatograph_logging
import pycatalicism.chromatograph.modbus_converter as convert
from pycatalicism.chromatograph.chromatograph_exceptions import ChromatographException

class WorkingStatus(Enum):
    """
    Working status of chromatograph and corresponding values in modbus protocol
    """
    NULL = 0
    PREPARATION = 1
    READY_FOR_ANALYSIS = 4
    PURGING = 6
    COOLING = 8
    ANALYSIS = 9

class ConnectionStatus(Enum):
    """
    Connection status of chromatograph and corresponding values in modbus protocol
    """
    CP_ON_CONNECTED = 7
    CP_ON_NOT_CONNECTED = 1
    CP_OFF_NOT_CONNECTED = 0

class ChromatographCommand(Enum):
    """
    Commands for chromatograph control and corresponding values in modbus protocol
    """
    CONNECT_CHROMATOGRAPH = 1
    START_ANALYSIS = 6

class ApplicationCommand(Enum):
    """
    Commands for application control and corresponding values in modbus protocol
    """
    START_CONTROL_PANEL = 1

class ChromatecControlPanelModbus():
    """
    Class represents simplified version of modbus protocol for connection with chromatec control panel modbus slave.
    """

    def __init__(self, modbus_id:int, working_status_input_address:int, serial_number_input_address:int, connection_status_input_address:int, method_holding_address:int, chromatograph_command_holding_address:int, application_command_holding_address:int, request_trials:int=3):
        """
        Initializes instance private variables, creates modbus client and registers logger.

        parameters
        ----------
        modbus_id:int
            modbus slave id of control panel software
        working_status_input_address:int
            modbus address of current chromatograph status (analysis, purging, preparing etc.)
        serial_number_input_address:int
            modbus address with chromatograph serial number
        connection_status_input_address:int
            modbus address for chromatograph and its applications connection status
        method_holding_address:int
            modbus address for setting instrumental methods
        chromatograph_command_holding_address:int
            modbus address for chromatograph commands (see chromatec modbus manual for details)
        application_command_holding_address:int
            modbus address for application commands (see chromatec modbus manual for details)
        """
        self._modbus_id = modbus_id
        self._request_trials = request_trials
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
        Get working status of chromatograph, i.e. analysis, purging, preparing etc.

        returns
        -------
        current_status:WorkingStatus
            one of the constants defined in WorkingStatus enum
        """
        count = 0
        while True:
            self._logger.debug(f'Getting current working status of chromatograph. Trial #{count}')
            try:
                response = self._modbus_client.read_input_registers(address=self._working_status_input_address, count=2, unit=self._modbus_id)
                response_registers = response.registers
                break
            except AttributeError:
                if count == self._request_trials-1:
                    raise ChromatographException('Cannot get working status!')
                else:
                    count += 1
        current_status_id = convert.bytes_to_int(response_registers)
        current_status = WorkingStatus(current_status_id)
        self._logger.log(5, f'{current_status = }')
        return current_status

    def get_serial_number(self) -> str:
        """
        Get serial number of chromatograph.

        returns
        -------
        serial_number:str
            serial number of chromatograph
        """
        count = 0
        while True:
            self._logger.debug(f'Getting chromatograph serial number. Trial #{count}')
            try:
                response = self._modbus_client.read_input_registers(address=self._serial_number_input_address, count=15, unit=self._modbus_id)
                response_registers = response.registers
                break
            except AttributeError:
                if count == self._request_trials-1:
                    raise ChromatographException('Cannot get serial number!')
                else:
                    count += 1
        serial_number = convert.bytes_to_string(response_registers)
        self._logger.log(5, f'{serial_number = }')
        return serial_number

    def get_connection_status(self) -> ConnectionStatus:
        """
        Get status of connection with chromatograph and control panel modbus slave.

        returns
        -------
        connection_status:ConnectionStatus
            one of the constants defined in ConnectionStatus enum
        """
        count = 0
        while True:
            self._logger.debug(f'Getting chromatograph and control panel connection status. Trial #{count}')
            try:
                response = self._modbus_client.read_input_registers(address=self._connection_status_input_address, count=1, unit=self._modbus_id)
                response_registers = response.registers
                break
            except AttributeError:
                if count == self._request_trials-1:
                    raise ChromatographException('Cannot get connection status!')
                else:
                    count += 1
        connection_status = ConnectionStatus(response_registers[0])
        self._logger.log(5, f'{connection_status = }')
        return connection_status

    def set_instrument_method(self, method_id:int):
        """
        Sets instrumental method to specified method id.

        parameters
        ----------
        method_id:int
            sequential number of instrumental method
        """
        self._logger.debug(f'Setting instrumental method to {method_id}')
        self._modbus_client.write_registers(address=self._method_holding_address, values=[method_id], unit=self._modbus_id)

    def send_chromatograph_command(self, command:ChromatographCommand):
        """
        Send command to chromatograph.

        parameters
        ----------
        command:ChromatographCommand
            one of the constants defined in ChromatographCommand enum
        """
        self._logger.debug(f'Sending command to chromatograph: {command}')
        self._modbus_client.write_registers(address=self._chromatograph_command_holding_address, values=[command.value], unit=self._modbus_id)

    def send_application_command(self, command:ApplicationCommand):
        """
        Send command to control panel application.

        parameters
        ----------
        command:ApplicationCommand
            one of the constants defined in ApplicationCommand enum
        """
        self._logger.debug(f'Sending command to control panel: {command}')
        self._modbus_client.write_registers(address=self._application_command_holding_address, values=[command.value], unit=self._modbus_id)
