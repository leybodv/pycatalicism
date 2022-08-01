import time

from pymodbus.client.sync import ModbusTcpClient

from pycatalicism.chromatograph.chromatograph import Chromatograph
from pycatalicism.chromatograph.chromatograph_exceptions import ChromatographModbusException

class ChromatecCrystal5000(Chromatograph):
    """
    """

    def __init__(self, control_panel_id:int, analytics_id:int, serial_id:str, methods:dict[str,int], chromatograph_command_address:int, application_command_address:int, chromatograph_serial_id_address:int, set_method_address:int, current_step_address:int):
        """
        """
        self.control_panel_id = control_panel_id
        self.analytics_id = analytics_id
        self.serial_id = serial_id
        self.methods = methods
        self.chromatograph_command_address = chromatograph_command_address
        self.application_command_address = application_command_address
        self.chromatograph_serial_id_address = chromatograph_serial_id_address
        self.set_method_address = set_method_address
        self.current_step_address = current_step_address
        self.modbus_client = None

    def connect(self) -> bool:
        """
        """
        self.modbus_client = ModbusTcpClient()
        self.modbus_client.write_registers(address=self.application_command_address, values=[1], unit=self.control_panel_id) # start control panel
        response = self.modbus_client.read_input_registers(address=self.chromatograph_serial_id_address, count=15, unit=self.control_panel_id)
        serial_id = self._bytes_to_string(response.registers)
        return serial_id == self.serial_id

    def set_instrument_method(self, method:str):
        """
        """
        if not self.modbus_client:
            raise ChromatographModbusException('Chromatograph is not connected')
        self.modbus_client.write_registers(address=self.set_method_address, values=[self.methods[method]], unit=self.control_panel_id)

    def start_analysis(self):
        """
        """
        if not self.modbus_client:
            raise ChromatographModbusException('Chromatograph is not connected')
        if self.is_ready_for_analysis():
            self.modbus_client.write_registers(address=self.chromatograph_command_address, values=[4], unit=self.control_panel_id) # NB: check correctness of written value, maybe values=[6] is correct
            # add information about sample
        else:
            # fire warning
            pass
        raise NotImplementedError()

    def is_ready_for_analysis(self) -> bool:
        """
        """
        if not self.modbus_client:
            raise ChromatographModbusException('Chromatograph is not connected')
        response = self.modbus_client.read_input_registers(address=self.current_step_address, count=2, unit=self.control_panel_id)
        step = self._bytes_to_int(response.registers)
        return step == 4

    def _bytes_to_string(self, response_bytes:list[int]) -> str:
        """
        """
        string = b''
        for b in response_bytes:
            string += b.to_bytes(2, 'big')
        string = string.decode().rstrip('\x00')
        return string
