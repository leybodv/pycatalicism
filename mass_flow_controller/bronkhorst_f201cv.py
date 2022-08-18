import propar

from pycatalicism.mass_flow_controller.mfc_exceptions import MFCConnectionException
from pycatalicism.mass_flow_controller.mfc_exceptions import MFCStateException
from pycatalicism.mass_flow_controller.bronkhorst_mfc_calibration import BronkhorstMFCCalibration
import pycatalicism.mass_flow_controller.mass_flow_controller_logging as mfc_logging

class BronkhorstF201CV():
    """
    """

    def __init__(self, serial_address:str, serial_id:str, calibrations:dict[int, BronkhorstMFCCalibration]):
        """
        """
        self._propar_instrument = propar.instrument(comport=serial_address)
        self._serial_id = serial_id
        self._calibrations = calibrations
        self._current_calibration = None
        self._connected = False
        self._logger = mfc_logging.get_logger(self.__class__.__name__)

    def connect(self):
        """
        """
        self._logger.info(f'Connecting to mass flow controller {self._serial_id}')
        serial_id_response = self._propar_instrument.readParameter(dde_nr=92)
        self._logger.log(5, f'{serial_id_response = }')
        if not serial_id_response == self._serial_id:
            raise MFCConnectionException(f'Wrong serial {serial_id_response} was received from the device {self._serial_id}')
        self._current_calibration = self._propar_instrument.readParameter(dde_nr=24)
        self._logger.log(5, f'{self._current_calibration = }')
        self._logger.info(f'Current calibration: {self._calibrations[self._current_calibration]}')
        self._connected = True

    def set_flow_rate(self, flow_rate:float):
        """
        """
        if not self._connected:
            raise MFCStateException(f'Mass flow controller {self._serial_id} is not connected!')
        self._logger.info(f'Setting flow rate to {flow_rate} nml/min')
        percent_setpoint = flow_rate * 100 / self._calibrations[self._current_calibration].get_max_flow_rate()
        self._logger.log(5, f'{percent_setpoint = }')
        propar_setpoint = int(percent_setpoint * 32000 / 100)
        self._logger.log(5, f'{propar_setpoint = }')
        self._propar_instrument.setpoint = propar_setpoint

    def set_calibration(self, calibration_num:int):
        """
        """
        if not self._connected:
            raise MFCStateException(f'Mass flow controller {self._serial_id} is not connected!')
        self._logger.info(f'Setting calibration to {self._calibrations[calibration_num]}')
        self._propar_instrument.writeParameter(dde_nr=24, data=calibration_num)
        self._current_calibration = calibration_num

    def get_flow_rate(self) -> float:
        """
        """
        if not self._connected:
            raise MFCStateException(f'Mass flow controller {self._serial_id} is not connected!')
        self._logger.info('Reading current flow rate')
        flow_rate_propar = self._propar_instrument.measure
        self._logger.log(5, f'{flow_rate_propar = }')
        if not flow_rate_propar:
            raise MFCConnectionException(f'Failed to get flow rate from the instrument {self._serial_id}')
        flow_rate_percent = flow_rate_propar / 32000.0
        self._logger.log(5, f'{flow_rate_percent = }')
        flow_rate = flow_rate_percent * self._calibrations[self._current_calibration].get_max_flow_rate()
        self._logger.log(5, f'{flow_rate = }')
        return flow_rate

    def get_calibration(self) -> BronkhorstMFCCalibration:
        """
        """
        if not self._connected:
            raise MFCStateException(f'Mass flow controller {self._serial_id} is not connected!')
        self._logger.info('Getting current calibration')
        calibration = self._calibrations[self._current_calibration]
        self._logger.log(5, f'{calibration = }')
        return calibration
