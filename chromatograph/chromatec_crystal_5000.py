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

    def connect(self):
        """
        """
        raise NotImplementedError()

    def set_method(self, method:str):
        """
        """
        raise NotImplementedError()

    def is_ready_for_analysis(self) -> bool:
        """
        """
        raise NotImplementedError()

    def start_analysis(self):
        """
        """
        raise NotImplementedError()

    def set_passport(self):
        """
        """
        raise NotImplementedError()
