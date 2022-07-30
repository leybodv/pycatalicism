from pymodbus.client.sync import ModbusTcpClient

from pycatalicism.chromatograph.chromatograph import Chromatograph

class ChromatecCrystal5000(Chromatograph):
    """
    """

    def __init__(self, control_panel_id:int, analytics_id:int):
        """
        """
        self.control_panel_id = control_panel_id
        self.analytics_id = analytics_id

    def connect(self) -> bool:
        """
        """
        # establish connection
        self.modbus_client = ModbusTcpClient()
        # start control panel
        # start analytics
        # check serial
