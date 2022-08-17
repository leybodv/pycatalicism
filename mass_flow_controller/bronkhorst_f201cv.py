import propar

class BronkhorstF201CV():
    """
    """

    def connect(self):
        """
        """
        serial_response = self._propar_intrument.readParameter(dde_nr=92)
        if not serial_response == self._serial:
            raise MFCConnectionException(f'Wrong serial {serial_response} was received from the device {self._serial}')
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
