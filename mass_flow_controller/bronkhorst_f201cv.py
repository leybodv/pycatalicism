import propar

from pycatalicism.mass_flow_controller.mfc_exceptions import MFCConnectionException
from pycatalicism.mass_flow_controller.mfc_exceptions import MFCStateException
from pycatalicism.mass_flow_controller.bronkhorst_mfc_calibration import BronkhorstMFCCalibration

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

    def connect(self):
        """
        """
        serial_id_response = self._propar_instrument.readParameter(dde_nr=92)
        if not serial_id_response == self._serial_id:
            raise MFCConnectionException(f'Wrong serial {serial_id_response} was received from the device {self._serial_id}')
        self._current_calibration = self._propar_instrument.readParameter(dde_nr=24)
        self._connected = True

    def set_flow_rate(self, flow_rate:float):
        """
        """
        if not self._connected:
            raise MFCStateException(f'Mass flow controller {self._serial_id} is not connected!')
        percent_setpoint = flow_rate * 100 / self._calibrations[self._current_calibration].get_max_flow_rate()
        propar_setpoint = int(percent_setpoint * 32000 / 100)
        self._propar_instrument.setpoint = propar_setpoint

    def set_calibration(self, calibration_num:int):
        """
        """
        if not self._connected:
            raise MFCStateException(f'Mass flow controller {self._serial_id} is not connected!')
        self._propar_instrument.writeParameter(dde_nr=24, data=calibration_num)
        self._current_calibration = calibration_num

    def get_flow_rate(self):
        """
        """
        raise NotImplementedError()

    def get_calibration(self):
        """
        """
        raise NotImplementedError()
