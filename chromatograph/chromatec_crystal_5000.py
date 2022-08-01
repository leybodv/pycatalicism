from pymodbus.client.sync import ModbusTcpClient

from pycatalicism.chromatograph.chromatograph import Chromatograph

class ChromatecCrystal5000(Chromatograph):
    """
    """

    def __init__(self, control_panel_id:int, analytics_id:int, serial_id:str, chromatograph_command_address:int, application_command_address:int):
        """
        """
        self.control_panel_id = control_panel_id
        self.analytics_id = analytics_id
        self.serial_id = serial_id
        self.chromatograph_command_address = chromatograph_command_address
        self.application_command_address = application_command_address

    def connect(self) -> bool:
        """
        """
        self.modbus_client = ModbusTcpClient()
        self.modbus_client.write_registers(address=self.chromatograph_command_address, values=[1], unit=self.control_panel_id) # establish connection with chromatograph
        self.modbus_client.write_registers(address=self.application_command_address, values=[1], unit=self.control_panel_id) # start control panel
        self.modbus_client.write_registers(address=self.application_command_address, values=[5], unit=self.control_panel_id) # start analytics
        serial_id = self._get_string()
        return serial_id == self.serial_id
