from enum import Enum

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

    def get_current_working_status(self) -> WorkingStatus:
        """
        """
        raise NotImplementedError()

    def get_serial_number(self) -> str:
        """
        """
        raise NotImplementedError()

    def get_connection_status(self) -> ConnectionStatus:
        """
        """
        raise NotImplementedError()

    def set_instrument_method(self, method_id:int):
        """
        """
        raise NotImplementedError()

    def send_chromatograph_command(self, command:ChromatographCommand):
        """
        """
        raise NotImplementedError()

    def send_application_command(self, command:ApplicationCommand):
        """
        """
        raise NotImplementedError()
