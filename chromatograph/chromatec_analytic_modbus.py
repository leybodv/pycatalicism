from enum import Enum

from pymodbus.client.sync import ModbusTcpClient

import pycatalicism.chromatograph.chromatograph_logging as chromatograph_logging
import pycatalicism.chromatograph.modbus_converter as convert

class ChromatogramPurpose(Enum):
    """
    """
    ANALYSIS = 0
    GRADUATION = 1

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
        self._logger.debug(f'Setting chromatogram name to {name}')
        name_bytes = convert.string_to_bytes(name)
        self._modbus_client.write_registers(address=self._sample_name_holding_address, values=name_bytes, unit=self._modbus_id)

    def set_chromatogram_purpose(self, purpose:ChromatogramPurpose):
        """
        """
        self._logger.debug(f'Setting chromatogram purpose to {purpose}')
        purpose_bytes = convert.int_to_bytes(purpose.value)
        self._modbus_client.write_registers(address=self._chromatogram_purpose_holding_address, values=purpose_bytes, unit=self._modbus_id)

    def set_sample_volume(self, volume:float):
        """
        """
        self._logger.debug(f'Setting sample volume to {volume}')
        volume_bytes = convert.double_to_bytes(volume)
        self._modbus_client.write_registers(address=self._sample_volume_holding_address, values=volume_bytes, unit=self._modbus_id)

    def set_sample_dilution(self, dilution:float):
        """
        """
        self._logger.debug(f'Setting sample dilution to {dilution}')
        dilution_bytes = convert.double_to_bytes(dilution)
        self._modbus_client.write_registers(address=self._sample_dilution_holding_address, values=dilution_bytes, unit=self._modbus_id)

    def set_operator(self, operator:str):
        """
        """
        self._logger.debug(f'Setting operator to {operator}')
        operator_bytes = convert.string_to_bytes(operator)
        self._modbus_client.write_registers(address=self._operator_holding_address, values=operator_bytes, unit=self._modbus_id)

    def set_column(self, column:str):
        """
        """
        self._logger.debug(f'Setting column to {column}')
        column_bytes = convert.string_to_bytes(column)
        self._modbus_client.write_registers(address=self._column_holding_address, values=column_bytes, unit=self._modbus_id)

    def set_lab_name(self, name:str):
        """
        """
        self._logger.debug(f'Setting laboratory name to {name}')
        name_bytes = convert.string_to_bytes(name)
        self._modbus_client.write_registers(address=self._lab_name_holding_address, values=name_bytes, unit=self._modbus_id)

    def get_lab_name(self) -> str:
        """
        """
        self._logger.debug('Getting laboratory name')
        response = self._modbus_client.read_holding_registers(address=self._lab_name_holding_address, count=15, unit=self._modbus_id)
        name = convert.bytes_to_string(response.registers)
        self._logger.log(5, f'{name = }')
        return name
