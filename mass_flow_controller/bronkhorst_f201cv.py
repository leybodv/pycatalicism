import propar

from pycatalicism.mass_flow_controller.mfc_exceptions import MFCConnectionException

class BronkhorstF201CV():
    """
    """

    def __init__(self, serial_address:str, serial_id:str):
        """
        """
        self._propar_intrument = propar.instrument(comport=serial_address)
        self._serial_id = serial_id
        self._connected = False

    def connect(self):
        """
        """
        serial_id_response = self._propar_intrument.readParameter(dde_nr=92)
        if not serial_id_response == self._serial_id:
            raise MFCConnectionException(f'Wrong serial {serial_id_response} was received from the device {self._serial_id}')
        self._connected = True

    def set_flow_rate(self):
        """
        """
        raise NotImplementedError()

    def set_calibration(self):
        """
        """
        raise NotImplementedError()

    def get_flow_rate(self):
        """
        """
        raise NotImplementedError()

    def get_calibration(self):
        """
        """
        raise NotImplementedError()
