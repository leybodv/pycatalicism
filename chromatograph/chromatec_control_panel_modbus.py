class ChromatecControlPanelModbus():
    """
    """

    def __init__(self, modbus_id:int, current_step_input_address:int, serial_number_input_address:int, connection_status_input_address:int, method_holding_address:int, chromatograph_command_holding_address:int, application_command_holding_address:int):
        """
        """
        self._modbus_id = modbus_id
        self._current_step_input_address = current_step_input_address
        self._serial_number_input_address = serial_number_input_address
        self._connection_status_input_address = connection_status_input_address
        self._method_holding_address = method_holding_address
        self._chromatograph_command_holding_address = chromatograph_command_holding_address
        self._application_command_holding_address = application_command_holding_address

    def get_current_step(self) -> CurrentStep:
        """
        """
        raise NotImplementedError()
