class BronkhorstMFCCalibration():
    """
    """

    def __init__(self, max_flow_rate:float, gas:str, p_in:float, p_out:float):
        """
        """
        self._max_flow_rate = max_flow_rate
        self._gas = gas
        self._p_in = p_in
        self._p_out = p_out

    def __str__(self) -> str:
        """
        """
        string = f'[gas: {self._gas}, p_in: {self._p_in}, p_out: {self._p_out}, flow rate: {self._max_flow_rate} nml/min]'
        return string

    def get_max_flow_rate(self) -> float:
        """
        """
        return self._max_flow_rate
