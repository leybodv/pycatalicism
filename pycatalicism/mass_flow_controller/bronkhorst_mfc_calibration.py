class BronkhorstMFCCalibration():
    """
    Class is a wrapper to mass flow controller calibration
    """

    def __init__(self, max_flow_rate:float, gas:str, p_in:float, p_out:float):
        """
        Initializes instance variables

        parameters
        ----------
        max_flow_rate:float
            Maximum flow rate in calibration in the units of mass flow controller
        gas:str
            Gas name
        p_in:float
            Pressure at the inlet of mass flow controller used in calibration
        p_out:float
            Pressure at the outlet of mass flow controller used in calibration
        """
        self._max_flow_rate = max_flow_rate
        self._gas = gas
        self._p_in = p_in
        self._p_out = p_out

    def __str__(self) -> str:
        """
        Get string representation of the object.

        returns
        -------
        string:str
            String representation of the calibration
        """
        string = f'[gas: {self._gas}, p_in: {self._p_in}, p_out: {self._p_out}, flow rate: {self._max_flow_rate} nml/min]'
        return string

    def get_max_flow_rate(self) -> float:
        """
        Get maximum flow rate of calibration in the units of mass flow controller

        returns
        -------
        max_flow_rate:float
            maximum flow rate
        """
        return self._max_flow_rate
