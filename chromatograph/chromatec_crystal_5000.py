import time
import struct

from pymodbus.client.sync import ModbusTcpClient

from pycatalicism.chromatograph.chromatograph import Chromatograph
from pycatalicism.chromatograph.chromatograph_exceptions import ChromatographModbusException

class ChromatecCrystal5000(Chromatograph):
    """
    """

    def __init__(self, control_panel_id:int, analytics_id:int, serial_id:str, lab_name:str, methods:dict[str,int], chromatograph_command_address:int, application_command_address:int, chromatograph_serial_id_address:int, set_method_address:int, current_step_address:int, connection_status_address:int, chromatogram_lab_name_address:int, chromatogram_name_address:int, chromatogram_sample_volume_address:int, chromatogram_sample_dilution_address:int, chromatogram_operator_address:int, chromatogram_column_address:int):
        """
        """
        self.control_panel_id = control_panel_id
        self.analytics_id = analytics_id
        self.serial_id = serial_id
        self.lab_name = lab_name
        self.methods = methods
        self.chromatograph_command_address = chromatograph_command_address
        self.application_command_address = application_command_address
        self.chromatograph_serial_id_address = chromatograph_serial_id_address
        self.set_method_address = set_method_address
        self.current_step_address = current_step_address
        self.connection_status_address = connection_status_address
        self.chromatogram_lab_name_address = chromatogram_lab_name_address
        self.chromatogram_name_address = chromatogram_name_address
        self.chromatogram_sample_volume_address = chromatogram_sample_volume_address
        self.chromatogram_sample_dilution_address = chromatogram_sample_dilution_address
        self.chromatogram_operator_address = chromatogram_operator_address
        self.chromatogram_column_address = chromatogram_column_address
        self.modbus_client = None

    def connect(self) -> bool:
        """
        check some register from chromatograph analytics also!
        """
        self.modbus_client = ModbusTcpClient()
        self.modbus_client.write_registers(address=self.application_command_address, values=[1], unit=self.control_panel_id)
        while True:
            response = self.modbus_client.read_input_registers(address=self.connection_status_address, count=1, unit=self.control_panel_id)
            if response.registers[0] == 7:
                break
            time.sleep(1)
        control_panel_response = self.modbus_client.read_input_registers(address=self.chromatograph_serial_id_address, count=15, unit=self.control_panel_id)
        serial_id = self._bytes_to_string(control_panel_response.registers)
        analytics_response = self.modbus_client.read_input_registers(address=self.chromatogram_lab_name_address, count=15, unit=self.analytics_id)
        lab_name = self._bytes_to_string(analytics_response.registers)
        return serial_id == self.serial_id and lab_name == self.lab_name

    def set_instrument_method(self, method:str):
        """
        """
        if not self.modbus_client:
            raise ChromatographModbusException('Chromatograph is not connected')
        self.modbus_client.write_registers(address=self.set_method_address, values=[self.methods[method]], unit=self.control_panel_id)

    def start_analysis(self, chromatogram_name:str, chromatogram_sample_volume:float, chromatogram_sample_dilution:float, chromatogram_operator:str, chromatogram_column:str):
        """
        In order to start analysis we need either write 6 to chromatograph_command_address register, set method, wait until chromatograph is ready for analysis, write 6 to chromatograph_command_address again OR arrange register addresses such that set_method_address is lower than chromatograph_command_address
        """
        if not self.modbus_client:
            raise ChromatographModbusException('Chromatograph is not connected')
        while True:
            if self.is_ready_for_analysis():
                break
            time.sleep(60)
        self.modbus_client.write_registers(address=self.chromatograph_command_address, values=[6], unit=self.control_panel_id)
        while True:
            response = self.modbus_client.read_input_registers(address=self.current_step_address, count=2, unit=self.control_panel_id)
            step = self._bytes_to_int(response.registers)
            if step != 9:
                break
            time.sleep(60)
        self.modbus_client.write_registers(address=self.chromatogram_name_address, values=self._string_to_bytes(chromatogram_name), unit=self.analytics_id)
        self.modbus_client.write_registers(address=self.chromatogram_sample_volume_address, values=self._double_to_bytes(chromatogram_sample_volume), unit=self.analytics_id)
        self.modbus_client.write_registers(address=self.chromatogram_sample_dilution_address, values=self._double_to_bytes(chromatogram_sample_dilution), unit=self.analytics_id)
        self.modbus_client.write_registers(address=self.chromatogram_operator_address, values=self._string_to_bytes(chromatogram_operator), unit=self.analytics_id)
        self.modbus_client.write_registers(address=self.chromatogram_column_address, values=self._string_to_bytes(chromatogram_column), unit=self.analytics_id)
        self.modbus_client.write_registers(address=self.chromatogram_lab_name_address, values=self._string_to_bytes(self.lab_name), unit=self.analytics_id)

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

    def _bytes_to_int(self, response_bytes:list[int]) -> int:
        """
        """
        return response_bytes[0]

    def _string_to_bytes(self, string:str) -> tuple[int]:
        """
        """
        if len(string) > 30:
            # log warning, string will be cut down to 30 chars
            string = string[0:30]
        if len(string) % 2 != 0:
            string += '\x00'
        string_bytes = bytes(string.encode())
        message = struct.unpack('>'+'H'*int(len(string_bytes)/2), string_bytes)
        return message

    def _double_to_bytes(self, double:float) -> tuple[int]:
        """
        """
        double_bytes = struct.pack('<d', double)
        message = struct.unpack('<HHHH', double_bytes)
        return message
