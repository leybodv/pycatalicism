import time

import pycatalicism.chromatograph.chromatograph_logging as chromatograph_logging
from pycatalicism.chromatograph.chromatec_control_panel_modbus import ChromatecControlPanelModbus
from pycatalicism.chromatograph.chromatec_control_panel_modbus import ConnectionStatus
from pycatalicism.chromatograph.chromatec_control_panel_modbus import WorkingStatus
from pycatalicism.chromatograph.chromatec_control_panel_modbus import ChromatographCommand
from pycatalicism.chromatograph.chromatec_control_panel_modbus import ApplicationCommand
from pycatalicism.chromatograph.chromatec_analytic_modbus import ChromatogramPurpose
from pycatalicism.chromatograph.chromatec_analytic_modbus import ChromatecAnalyticModbus
from pycatalicism.chromatograph.chromatograph_exceptions import ChromatographException
from pycatalicism.chromatograph.chromatograph_exceptions import ChromatographStateException

class ChromatecCrystal5000():
    """
    Class represents chromatec crystal 5000 chromatograph. Communication is done via modbus protocol.
    """

    def __init__(self, control_panel:ChromatecControlPanelModbus, analytic:ChromatecAnalyticModbus, methods:dict[str, int]):
        """
        Initializes instance variables, registers logger.
        """
        self._control_panel = control_panel
        self._analytic = analytic
        self._methods = methods
        self._logger = chromatograph_logging.get_logger(self.__class__.__name__)
        self._connected = False

    def connect(self):
        """
        Connect to chromatograph. If chromatec control panel is not up, start control panel, connection is established automatically in this case. If control panel is up, but chromatograph is disconnected, establish connection. Do nothing otherwise.

        raises
        ------
        ChromatographException
            if unknown connection status was get from chromatograph
        """
        connection_status = self._control_panel.get_connection_status()
        if connection_status is ConnectionStatus.CP_OFF_NOT_CONNECTED:
            self._logger.info('Starting control panel application')
            self._control_panel.send_application_command(ApplicationCommand.START_CONTROL_PANEL)
            self._logger.info('Waiting until control panel is up...')
            while True:
                connection_status = self._control_panel.get_connection_status()
                self._logger.debug(f'{connection_status = }')
                if connection_status is ConnectionStatus.CP_ON_CONNECTED:
                    break
                time.sleep(10)
            self._connected = True
            self._logger.info('Control panel is UP. Connection established.')
        elif connection_status is ConnectionStatus.CP_ON_NOT_CONNECTED:
            self._logger.info('Connecting to chromatograph')
            self._control_panel.send_chromatograph_command(ChromatographCommand.CONNECT_CHROMATOGRAPH)
            self._logger.info('Waiting until connection is established...')
            while True:
                connection_status = self._control_panel.get_connection_status()
                self._logger.debug(f'{connection_status = }')
                if connection_status is ConnectionStatus.CP_ON_CONNECTED:
                    break
                time.sleep(10)
            self._connected = True
            self._logger.info('Connection established')
        elif connection_status is ConnectionStatus.CP_ON_CONNECTED:
            self._logger.info('Chromatograph connected already')
            self._connected = True
        else:
            raise ChromatographException(f'Unknown connection status: {connection_status}')

    def set_method(self, method:str):
        """
        Set chromatograph instrument method. Chromatograph start to prepare itself for analysis accordingly.

        parameters
        ----------
        method:str
            method to send to chromatograph

        raises
        ------
        ChromatographStateException
            if connection to chromatograph is not established or analysis is in progress now
        """
        working_status = self._control_panel.get_current_working_status()
        if not self._connected:
            raise ChromatographStateException('Connect to chromatograph first!')
        if working_status is WorkingStatus.ANALYSIS:
            raise ChromatographStateException('Analysis is in progress!')
        self._logger.info(f'Setting method to {method}')
        self._control_panel.set_instrument_method(self._methods[method])

    def is_ready_for_analysis(self) -> bool:
        """
        Check if chromatograph is ready for analysis.

        returns
        -------
        is_ready_for_analysis:bool
            True if chromatograph is ready for analysis

        raises
        ------
        ChromatographStateException
            if connection to chromatograph is not established
        """
        working_status = self._control_panel.get_current_working_status()
        if not self._connected:
            raise ChromatographStateException('Connect to chromatograph first!')
        self._logger.info('Checking if chromatograph is ready for analysis')
        is_ready_for_analysis = working_status is WorkingStatus.READY_FOR_ANALYSIS
        self._logger.info(f'Chromatograph is ready for analysis: {is_ready_for_analysis}')
        return is_ready_for_analysis

    def start_analysis(self):
        """
        Start analysis.

        raises
        ------
        ChromatographStateException
            if chromatograph is not connected or instrumental method was not started yet or chromatograph is not ready to start analysis
        """
        working_status = self._control_panel.get_current_working_status()
        if not self._connected:
            raise ChromatographStateException('Connect to chromatograph first!')
        if working_status is WorkingStatus.NULL:
            raise ChromatographStateException('Start some instrumental method first!')
        if working_status is not WorkingStatus.READY_FOR_ANALYSIS:
            raise ChromatographStateException('Chromatograph is not ready to start analysis')
        else:
            self._logger.info('Starting analysis')
            self._control_panel.send_chromatograph_command(ChromatographCommand.START_ANALYSIS)

    def set_passport(self, name:str, volume:float, dilution:float, purpose:ChromatogramPurpose, operator:str, column:str, lab_name:str):
        """
        Set passport values for chromatogram. Method should be called after the analysis is finished otherwise previous chromatogram's passport will be changed.

        parameters
        ----------
        name:str
            name of chromatogram
        volume:float
            volume of sample
        dilution:float
            dilution of sample
        purpose:ChromatogramPurpose
            analysis or graduation
        operator:str
            name of operator
        column:str
            name of column
        lab_name:str
            name of laboratory

        raises
        ------
        ChromatographStateException
            if chromatograph is not connected or method was not started yet or analysis is in progress
        """
        working_status = self._control_panel.get_current_working_status()
        if not self._connected:
            raise ChromatographStateException('Connect chromatograph first!')
        if working_status is WorkingStatus.NULL:
            raise ChromatographStateException('Start some instrumental method first!')
        if working_status is WorkingStatus.ANALYSIS:
            raise ChromatographStateException('Analysis is in progress, cannot set passport for currently running chromatogram, wait until analysis is over!')
        self._analytic.set_sample_name(name)
        self._analytic.set_sample_volume(volume)
        self._analytic.set_sample_dilution(dilution)
        self._analytic.set_chromatogram_purpose(purpose)
        self._analytic.set_operator(operator)
        self._analytic.set_column(column)
        self._analytic.set_lab_name(lab_name)

    def get_working_status(self) -> WorkingStatus:
        """
        Get working status of chromatograph.

        returns
        -------
        working_status:WorkingStatus
            chromatograph working status

        raises
        ------
        ChromatographStateException
            if chromatograph is not connected
        """
        if not self._connected:
            raise ChromatographStateException('Connect chromatograph first!')
        self._logger.info('Getting working status.')
        working_status = self._control_panel.get_current_working_status()
        self._logger.debug(f'{working_status = }')
        return working_status
