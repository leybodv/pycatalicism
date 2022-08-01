from pymodbus.client.sync import ModbusTcpClient

from pycatalicism.chromatograph.chromatograph import Chromatograph
from pycatalicism.chromatograph.chromatograph_exceptions import ChromatographModbusException

class ChromatecCrystal5000(Chromatograph):
    """
    """

    def __init__(self, control_panel_id:int, analytics_id:int, serial_id:str, chromatograph_command_address:int, application_command_address:int, chromatograph_serial_id_address:int):
        """
        """
        self.control_panel_id = control_panel_id
        self.analytics_id = analytics_id
        self.serial_id = serial_id
        self.chromatograph_command_address = chromatograph_command_address
        self.application_command_address = application_command_address
        self.chromatograph_serial_id_address = chromatograph_serial_id_address

    def connect(self) -> bool:
        """
        """
        self.modbus_client = ModbusTcpClient()
        self.modbus_client.write_registers(address=self.application_command_address, values=[1], unit=self.control_panel_id) # start control panel
        serial_id = self._get_string(register_type='input', address=self.chromatograph_serial_id_address, count=15, unit=self.control_panel_id)
        return serial_id == self.serial_id

    def _get_string(self, register_type:str, address:int, count:int, unit:int) -> str:
        """
        """
        if register_type == 'input':
            response = self.modbus_client.read_input_registers(address=address, count=count, unit=unit)
            string = b''
            for b in response.registers:
                string += b.to_bytes(2, 'big')
            string = string.decode().rstrip('\x00')
        else:
            raise ChromatographModbusException(f'Unknown type of register to read from: {register_type}')
        return string
