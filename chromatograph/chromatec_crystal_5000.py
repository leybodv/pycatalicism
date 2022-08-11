import pycatalicism.chromatograph.chromatograph_logging as chromatograph_logging
from pycatalicism.chromatograph.chromatec_control_panel_modbus import ChromatecControlPanelModbus
from pycatalicism.chromatograph.chromatec_analytic_modbus import ChromatecAnalyticModbus

class ChromatecCrystal5000():
    """
    """

    def __init__(self, control_panel:ChromatecControlPanelModbus, analytic:ChromatecAnalyticModbus):
        """
        """
        self._control_panel = control_panel
        self._analytic = analytic
        self._logger = chromatograph_logging.get_logger(self.__class__.__name__)
