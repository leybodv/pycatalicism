from enum import Enum
import threading

from pymodbus.client.sync import ModbusTcpClient

import pycatalicism.chromatograph.chromatograph_logging as chromatograph_logging
import pycatalicism.chromatograph.modbus_converter as convert

class ChromatogramPurpose(Enum):
    """
    Prupose of chromatogram as is written in passport
    """
    ANALYSIS = 0
    GRADUATION = 1

class ChromatecAnalyticModbus():
    """
    Class represents modbus protocol for connection with chromatec analytic modbus slave
    """

    def __init__(self, modbus_id:int, sample_name_holding_address:int, chromatogram_purpose_holding_address:int, sample_volume_holding_address:int, sample_dilution_holding_address:int, operator_holding_address:int, column_holding_address:int, lab_name_holding_address:int):
        """
        Initializes private instance variables. Registers logger.

        parameters
        ----------
        modbus_id:int
            modbus slave id of analytic software
        sample_name_holding_address:int
            modbus address for chromatogram name as written in the passport of chromatogram
        chromatogram_purpose_holding_address:int
            modbus address for chromatogram purpose as written in the passport of chromatogram
        sample_volume_holding_address:int
            modbus address for sample volume as written in the passport of chromatogram
        sample_dilution_holding_address:int
            modbus address for sample dilution as written in the passport of chromatogram
        operator_holding_address:int
            modbus address for operator as written in the passport of chromatogram
        column_holding_address:int
            modbus address for column as written in the passport of chromatogram
        lab_name_holding_address:int
            modbus address for lab name as written in the passport of chromatogram
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
        self._read_write_lock = threading.Lock()
        self._logger = chromatograph_logging.get_logger(self.__class__.__name__)

    def set_sample_name(self, name:str):
        """
        Set name of sample in chromatogram's passport.

        parameters
        ----------
        name:str
            name of sample
        """
        self._logger.debug(f'Setting chromatogram name to {name}')
        name_bytes = convert.string_to_bytes(name)
        with self._read_write_lock:
            self._modbus_client.write_registers(address=self._sample_name_holding_address, values=name_bytes, unit=self._modbus_id)

    def set_chromatogram_purpose(self, purpose:ChromatogramPurpose):
        """
        Set purpose of chromatogram in chromatogram's passport.

        parameters
        ----------
        purpose:ChromatogramPurpose
            one of the constants defined in ChromatogramPurpose enum
        """
        self._logger.debug(f'Setting chromatogram purpose to {purpose}')
        purpose_bytes = convert.int_to_bytes(purpose.value)
        with self._read_write_lock:
            self._modbus_client.write_registers(address=self._chromatogram_purpose_holding_address, values=purpose_bytes, unit=self._modbus_id)

    def set_sample_volume(self, volume:float):
        """
        Set sample volume in chromatogram's passport.

        parameters
        ----------
        volume:float
            sample volume
        """
        self._logger.debug(f'Setting sample volume to {volume}')
        volume_bytes = convert.double_to_bytes(volume)
        with self._read_write_lock:
            self._modbus_client.write_registers(address=self._sample_volume_holding_address, values=volume_bytes, unit=self._modbus_id)

    def set_sample_dilution(self, dilution:float):
        """
        Set sample dilution in chromatogram's passport.

        parameters
        ----------
        dilution:float
            sample dilution
        """
        self._logger.debug(f'Setting sample dilution to {dilution}')
        dilution_bytes = convert.double_to_bytes(dilution)
        with self._read_write_lock:
            self._modbus_client.write_registers(address=self._sample_dilution_holding_address, values=dilution_bytes, unit=self._modbus_id)

    def set_operator(self, operator:str):
        """
        Set operator in chromatogram's passport.

        parameters
        ----------
        operator:str
            operator's name
        """
        self._logger.debug(f'Setting operator to {operator}')
        operator_bytes = convert.string_to_bytes(operator)
        with self._read_write_lock:
            self._modbus_client.write_registers(address=self._operator_holding_address, values=operator_bytes, unit=self._modbus_id)

    def set_column(self, column:str):
        """
        Set column in chromatogram's passport.

        parameters
        ----------
        column:str
            column's name
        """
        self._logger.debug(f'Setting column to {column}')
        column_bytes = convert.string_to_bytes(column)
        with self._read_write_lock:
            self._modbus_client.write_registers(address=self._column_holding_address, values=column_bytes, unit=self._modbus_id)

    def set_lab_name(self, name:str):
        """
        Set laboratory name in chromatogram's passport

        parameters
        ----------
        name:str
            laboratory name
        """
        self._logger.debug(f'Setting laboratory name to {name}')
        name_bytes = convert.string_to_bytes(name)
        with self._read_write_lock:
            self._modbus_client.write_registers(address=self._lab_name_holding_address, values=name_bytes, unit=self._modbus_id)

    def get_lab_name(self) -> str:
        """
        Get laboratory name from chromatogram's passport.

        returns
        -------
        name:str
            laboratory name
        """
        self._logger.debug('Getting laboratory name')
        with self._read_write_lock:
            response = self._modbus_client.read_holding_registers(address=self._lab_name_holding_address, count=15, unit=self._modbus_id)
        name = convert.bytes_to_string(response.registers)
        self._logger.log(5, f'{name = }')
        return name
