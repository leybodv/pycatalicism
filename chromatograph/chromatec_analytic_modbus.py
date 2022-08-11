from pymodbus.client.sync import ModbusTcpClient

import pycatalicism.chromatograph.chromatograph_logging as chromatograph_logging

class ChromatecAnalyticModbus():
    """
    """

    def __init__(self, modbus_id:int, sample_name_holding_address:int, chromatogram_purpose_holding_address:int, sample_volume_holding_address:int, sample_dilution_holding_address:int, operator_holding_address:int, column_holding_address:int, lab_name_holding_address:int):
        """
        """
        self._modbus_id = modbus_id
        self._sample_name_holding_address = sample_name_holding_address
        self._chromatogram_purpose_holding_address = chromatogram_purpose_holding_address
        self._sample_volume_holding_address = sample_volume_holding_address
        self._sample_dilution_holding_address = sample_dilution_holding_address
        self._operator_holding_address = operator_holding_address
        self._column_holding_address = column_holding_address
        self._lab_name_holding_address = lab_name_holding_address
        self._modbus_client = ModbusTcpClient()
        self._logger = chromatograph_logging.get_logger(self.__class__.__name__)

    def set_sample_name(self, name:str):
        """
        """
        raise NotImplementedError()

    def set_chromatogram_purpose(self, purpose:ChromatogramPurpose):
        """
        """
        raise NotImplementedError()

    def set_sample_volume(self, volume:float):
        """
        """
        raise NotImplementedError()

    def set_sample_dilution(self, dilution:float):
        """
        """
        raise NotImplementedError()

    def set_operator(self, operator:str):
        """
        """
        raise NotImplementedError()

    def set_column(self, column:str):
        """
        """
        raise NotImplementedError()

    def set_lab_name(self, name:str):
        """
        """
        raise NotImplementedError()

    def get_lab_name(self) -> str:
        """
        """
        raise NotImplementedError()
