import propar

from mass_flow_controller.mfc_exceptions import MFCConnectionException
from mass_flow_controller.mfc_exceptions import MFCStateException
from mass_flow_controller.bronkhorst_mfc_calibration import BronkhorstMFCCalibration
import mass_flow_controller.mass_flow_controller_logging as mfc_logging

class BronkhorstF201CV():
    """
    Class represents Bronkhorst F201CV mass flow controller.
    """

    def __init__(self, serial_address:str, serial_id:str, calibrations:dict[int, BronkhorstMFCCalibration]):
        """
        Initializes instance variables, registers logger.

        parameters
        ----------
        serial_address:str
            serial address of this controller (COM or /dev/ttyUSB)
        serial_id:str
            serial number of this controller (e.g. M111202123A, see documentation)
        calibrations:dict[int, BronkhorstMFCCalibration]
            set of calibrations written in the memory of the device with corresponding calibration number. NB: calibration number is for propar protocol, numbering is started from 0, so fluid1 has 0th number
        """
        self._serial_address = serial_address
        self._serial_id = serial_id
        self._calibrations = calibrations
        self._current_calibration = None
        self._connected = False
        self._logger = mfc_logging.get_logger(self.__class__.__name__)

    def connect(self):
        """
        Connect to mass flow controller. Method requests serial number of the device and compares it with the one, provided at object creation. Also method requests current calibration number. This method must be run before any other method of the class.

        raises
        ------
        MFCConnectionException
            if wrong serial id was received from the device
        """
        self._logger.info(f'Connecting to mass flow controller {self._serial_id}')
        self._propar_instrument = propar.instrument(comport=self._serial_address)
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
        Sets flow rate to specified value.

        parameters
        ----------
        flow_rate:float
            flow rate in the units of mass flow controller

        raises
        ------
        MFCStateException
            if mass flow controller is not connected
        """
        if not self._connected:
            raise MFCStateException(f'Mass flow controller {self._serial_id} is not connected!')
        if flow_rate > self._calibrations[self._current_calibration].get_max_flow_rate():
            self._logger.warning('Cannot set flow rate bigger than maximum value in calibraion! Flow rate will be set to maximum value.')
            flow_rate = self._calibrations[self._current_calibration].get_max_flow_rate()
        self._logger.info(f'Setting flow rate to {flow_rate} nml/min')
        percent_setpoint = flow_rate * 100 / self._calibrations[self._current_calibration].get_max_flow_rate()
        self._logger.log(5, f'{percent_setpoint = }')
        propar_setpoint = int(percent_setpoint * 32000 / 100)
        self._logger.log(5, f'{propar_setpoint = }')
        self._propar_instrument.setpoint = propar_setpoint

    def set_calibration(self, calibration_num:int):
        """
        Set calibration to specified calibration number.

        parameters
        ----------
        calibration_num:int
            the number of calibration. NB: the numbering is started from 0, so calibration for fluid1 has 0th order.

        raises
        ------
        MFCStateException
            if mass flow controller is not connected
        """
        if not self._connected:
            raise MFCStateException(f'Mass flow controller {self._serial_id} is not connected!')
        self._logger.info(f'Setting calibration to {self._calibrations[calibration_num]}')
        self._propar_instrument.writeParameter(dde_nr=24, data=calibration_num)
        self._current_calibration = calibration_num

    def get_flow_rate(self) -> float:
        """
        Get current flow rate from mass flow controller.

        returns
        -------
        flow_rate:float
            flow rate in the units of mass flow controller

        raises
        ------
        MFCStateException
            if mass flow controller is not connected
        """
        if not self._connected:
            raise MFCStateException(f'Mass flow controller {self._serial_id} is not connected!')
        self._logger.info('Reading current flow rate')
        flow_rate_propar = self._propar_instrument.measure
        self._logger.log(5, f'{flow_rate_propar = }')
        if flow_rate_propar is None:
            raise MFCConnectionException(f'Failed to get flow rate from the instrument {self._serial_id}')
        flow_rate_percent = flow_rate_propar / 32000.0
        self._logger.log(5, f'{flow_rate_percent = }')
        flow_rate = flow_rate_percent * self._calibrations[self._current_calibration].get_max_flow_rate()
        self._logger.log(5, f'{flow_rate = }')
        return flow_rate

    def get_calibration(self) -> BronkhorstMFCCalibration:
        """
        Get current calibration set in mass flow controller.

        returns
        -------
        calibration:BronkhorstMFCCalibration
            wrapper with calibration data

        raises
        ------
        MFCStateException
            if mass flow controller is not connected
        """
        if not self._connected:
            raise MFCStateException(f'Mass flow controller {self._serial_id} is not connected!')
        self._logger.info('Getting current calibration')
        calibration = self._calibrations[self._current_calibration]
        self._logger.log(5, f'{calibration = }')
        return calibration
