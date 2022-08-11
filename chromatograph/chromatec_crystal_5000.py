import time

import pycatalicism.chromatograph.chromatograph_logging as chromatograph_logging
from pycatalicism.chromatograph.chromatec_control_panel_modbus import ChromatecControlPanelModbus
from pycatalicism.chromatograph.chromatec_control_panel_modbus import ConnectionStatus
from pycatalicism.chromatograph.chromatec_control_panel_modbus import WorkingStatus
from pycatalicism.chromatograph.chromatec_control_panel_modbus import ChromatographCommand
from pycatalicism.chromatograph.chromatec_control_panel_modbus import ApplicationCommand
from pycatalicism.chromatograph.chromatec_analytic_modbus import ChromatecAnalyticModbus
from pycatalicism.chromatograph.chromatograph_exceptions import ChromatographException
from pycatalicism.chromatograph.chromatograph_exceptions import ChromatographStateException

class ChromatecCrystal5000():
    """
    """

    def __init__(self, control_panel:ChromatecControlPanelModbus, analytic:ChromatecAnalyticModbus):
        """
        """
        self._control_panel = control_panel
        self._analytic = analytic
        self._logger = chromatograph_logging.get_logger(self.__class__.__name__)
        self._connection_status = control_panel.get_connection_status()
        self._working_status = control_panel.get_current_working_status()

    def connect(self):
        """
        Connect to chromatograph. If chromatec control panel is not up, start control panel, connection is established automatically in this case. If control panel is up, but chromatograph is disconnected, establish connection. Do nothing otherwise.

        raises
        ------
        ChromatographException
            if unknown connection status was get from chromatograph
        """
        if self._connection_status is ConnectionStatus.CP_OFF_NOT_CONNECTED:
            self._logger.info('Starting control panel application')
            self._control_panel.send_application_command(ApplicationCommand.START_CONTROL_PANEL)
            self._logger.info('Waiting until control panel is up...')
            while True:
                self._connection_status = self._control_panel.get_connection_status()
                self._logger.debug(f'{self._connection_status = }')
                if self._connection_status is ConnectionStatus.CP_ON_CONNECTED:
                    break
                time.sleep(1)
            self._logger.info('Control panel is UP. Connection established.')
        elif self._connection_status is ConnectionStatus.CP_ON_NOT_CONNECTED:
            self._logger.info('Connecting to chromatograph')
            self._control_panel.send_chromatograph_command(ChromatographCommand.CONNECT_CHROMATOGRAPH)
            self._logger.info('Waiting until connection is established...')
            while True:
                self._connection_status = self._control_panel.get_connection_status()
                self._logger.debug(f'{self._connection_status = }')
                if self._connection_status is ConnectionStatus.CP_ON_CONNECTED:
                    break
                time.sleep(1)
            self._logger.info('Connection established')
        elif self._connection_status is ConnectionStatus.CP_ON_CONNECTED:
            self._logger.info('Chromatograph connected already')
        else:
            raise ChromatographException(f'Unknown connection status: {self._connection_status}')
        self._working_status = self._control_panel.get_current_working_status()

    def set_method(self, method:str):
        """
        """
        if self._connection_status is not ConnectionStatus.CP_ON_CONNECTED:
            raise ChromatographStateException('Connect to chromatograph first!')
        if self._connection_status is WorkingStatus.ANALYSIS:
            raise ChromatographStateException('Analysis is in progress!')
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
