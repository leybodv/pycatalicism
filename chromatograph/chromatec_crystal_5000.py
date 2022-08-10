import time
import struct
from logging import Logger

from pymodbus.client.sync import ModbusTcpClient

from pycatalicism.chromatograph.chromatograph import Chromatograph
from pycatalicism.chromatograph.chromatograph_exceptions import ChromatographStateException

class ChromatecCrystal5000(Chromatograph):
    """
    Class represents Chromatec Crystal 5000 chromatograph communitacting through modbus protocol.
    """

    def __init__(self, control_panel_id:int, analytics_id:int, serial_id:str, lab_name:str, methods:dict[str,int], chromatograph_command_address:int, application_command_address:int, chromatograph_serial_id_address:int, set_method_address:int, current_step_address:int, connection_status_address:int, chromatogram_lab_name_address:int, chromatogram_name_address:int, chromatogram_sample_volume_address:int, chromatogram_sample_dilution_address:int, chromatogram_operator_address:int, chromatogram_column_address:int, logger:Logger|None):
        """
        Initializes instance variables based on the provided parameters.

        parameters
        ----------
        control_panel_id:int
            modbus slave id of control panel software
        analytics_id:int
            modbux slave id of analytics software
        serial_id:str
            serial number of chromatograph (used to ensure successful connection to control panel via modbus)
        lab_name:str
            lab name as must be written in every chromatogram passport (used to ensure successful connection to analytics via modbus)
        methods:dict[str,int]
            dictionary of instrumental methods used in control panel software with their corresponding number counted from 0, as they appear in a control panel
        chromatograph_command_address:int
            modbus address for chromatograph commands (see chromatec modbus manual for details)
        application_command_address:int
            modbus address for application commands (see chromatec modbus manual for details)
        chromatograph_serial_id_address:int
            modbus address with chromatograph serial number
        set_method_address:int
            modbus address for setting instrumental methods
        current_step_address:int
            modbus address of current chromatograph status (analysis, purging, preparing etc.)
        connection_status_address:int
            modbus address for chromatograph and its applications connection status
        chromatogram_lab_name_address:int
            modbus address for lab name as written in the passport of chromatogram
        chromatogram_name_address:int
            modbus address for chromatogram name as written in the passport of chromatogram
        chromatogram_sample_volume_address:int
            modbus address for sample volume as written in the passport of chromatogram
        chromatogram_sample_dilution_address:int
            modbus address for sample dilution as written in the passport of chromatogram
        chromatogram_operator_address:int
            modbus address for operator as written in the passport of chromatogram
        chromatogram_column_address:int
            modbus address for column as written in the passport of chromatogram
        logger:Logger|None
            logger for logging relevant information or None to disable logging
        """
        self.control_panel_id = control_panel_id
        self.analytics_id = analytics_id
        self.serial_id = serial_id
        self.lab_name = lab_name
        self.methods = methods
        self.chromatograph_command_address = chromatograph_command_address
        self.application_command_address = application_command_address
        self.chromatograph_serial_id_address = chromatograph_serial_id_address
        self.set_method_address = set_method_address
        self.current_step_address = current_step_address
        self.connection_status_address = connection_status_address
        self.chromatogram_lab_name_address = chromatogram_lab_name_address
        self.chromatogram_name_address = chromatogram_name_address
        self.chromatogram_sample_volume_address = chromatogram_sample_volume_address
        self.chromatogram_sample_dilution_address = chromatogram_sample_dilution_address
        self.chromatogram_operator_address = chromatogram_operator_address
        self.chromatogram_column_address = chromatogram_column_address
        self.modbus_client = None
        self.current_method = None
        if logger:
            self.logger = logger

    def connect(self) -> bool:
        """
        Connect to chromatograph. Method starts control panel and analytic software, waits until it is started and reads chromatograph serial number and laboratory name from control panel and analytic applications, respectively. NB: method hangs calling thread until chromatec applications are started and corresponding information is read.

        returns
        -------
        True if connection was successful
        """
        if self.logger:
            self.logger.info('Connecting to Chromatec Crystal 5000 chromatograph')
        self.modbus_client = ModbusTcpClient()
        if self.logger:
            self.logger.info('Starting control panel and analytic software')
        self.modbus_client.write_registers(address=self.application_command_address, values=[1], unit=self.control_panel_id)
        if self.logger:
            self.logger.info('Waiting for control panel and analytic software to start...')
        while True:
            response = self.modbus_client.read_input_registers(address=self.connection_status_address, count=1, unit=self.control_panel_id)
            if self.logger:
                self.logger.debug(f'Response from modbus: {response.registers}')
            if response.registers[0] == 7:
                break
            time.sleep(1)
        if self.logger:
            self.logger.info('Checking chromatograph serial number')
        control_panel_response = self.modbus_client.read_input_registers(address=self.chromatograph_serial_id_address, count=15, unit=self.control_panel_id)
        serial_id = self._bytes_to_string(control_panel_response.registers)
        if self.logger:
            self.logger.debug(f'Serial number received from chromatograph: {serial_id}')
            self.logger.info('Checking lab name from analytics software')
        analytics_response = self.modbus_client.read_input_registers(address=self.chromatogram_lab_name_address, count=15, unit=self.analytics_id)
        lab_name = self._bytes_to_string(analytics_response.registers)
        if self.logger:
            self.logger.debug(f'Laboratory name received from analytics software: {lab_name}')
        connection_is_successful = serial_id == self.serial_id and lab_name == self.lab_name
        if not connection_is_successful:
            self.modbus_client = None
        if self.logger:
            self.logger.info(f'Connection successful: {connection_is_successful}')
        return connection_is_successful

    def set_instrument_method(self, method:str):
        """
        Sets instrument method to specified value. Method changes the state of chromatograph to 'preparing' status.

        parameters
        ----------
        method:str
            instrument method to set for chromatograph, must be in self.methods instance variable

        raises
        ------
        ChromatographStateException
            if connect method was not called or if connection was unsuccessful
        """
        if not self.modbus_client:
            raise ChromatographStateException('Chromatograph is not connected')
        if self.logger:
            self.logger.info(f'Setting instrument method to {method}')
        self.modbus_client.write_registers(address=self.set_method_address, values=[self.methods[method]], unit=self.control_panel_id)
        self.current_method = method

    def start_analysis(self, chromatogram_name:str, chromatogram_sample_volume:float, chromatogram_sample_dilution:float, chromatogram_operator:str, chromatogram_column:str):
        """
        Start instrumental method. Method waits until chromatograph is ready for analysis, starts analysis, waits until it is completed and writes relevant information to chromatogram passport. NB: method blocks calling thread until it terminates.

        parameters
        ----------
        chromatogram_name:str
            name of chromatogram which will be written in passport
        chromatogram_sample_volume:float
            sample volume which will be written in passport
        chromatogram_sample_dilution:float
            sample dilution which will be written in passport
        chromatogram_operator:str
            operator's name which will be written in passport
        chromatogram_column:str
            column name which will be written in passport

        raises
        ------
        ChromatographStateException
            if connect method was not called or if connection was unsuccessful or if instrumental method was not set before
        """
        if not self.modbus_client:
            raise ChromatographStateException('Chromatograph is not connected')
        if not self.current_method:
            raise ChromatographStateException('Set method before starting the analysis')
        if self.logger:
            self.logger.info('Waiting while chromatograph is ready to start analysis')
        while True:
            if self.is_ready_for_analysis():
                break
            time.sleep(60)
        if self.logger:
            self.logger.info('Starting analysis')
        self.modbus_client.write_registers(address=self.chromatograph_command_address, values=[6], unit=self.control_panel_id)
        if self.logger:
            self.logger.info('Waiting until analysis is finished')
        while True:
            response = self.modbus_client.read_input_registers(address=self.current_step_address, count=2, unit=self.control_panel_id)
            step = self._bytes_to_int(response.registers)
            if self.logger:
                self.logger.debug(f'Current chromatograph status: {step}')
            if step != 9:
                break
            time.sleep(60)
        if self.logger:
            self.logger.info('Writing information about chromatogram')
        self.modbus_client.write_registers(address=self.chromatogram_name_address, values=self._string_to_bytes(chromatogram_name), unit=self.analytics_id)
        self.modbus_client.write_registers(address=self.chromatogram_sample_volume_address, values=self._double_to_bytes(chromatogram_sample_volume), unit=self.analytics_id)
        self.modbus_client.write_registers(address=self.chromatogram_sample_dilution_address, values=self._double_to_bytes(chromatogram_sample_dilution), unit=self.analytics_id)
        self.modbus_client.write_registers(address=self.chromatogram_operator_address, values=self._string_to_bytes(chromatogram_operator), unit=self.analytics_id)
        self.modbus_client.write_registers(address=self.chromatogram_column_address, values=self._string_to_bytes(chromatogram_column), unit=self.analytics_id)
        self.modbus_client.write_registers(address=self.chromatogram_lab_name_address, values=self._string_to_bytes(self.lab_name), unit=self.analytics_id)

    def is_ready_for_analysis(self) -> bool:
        """
        """
        if not self.modbus_client:
            raise ChromatographStateException('Chromatograph is not connected')
        if self.logger:
            self.logger.info('Checking if chromatograph is ready for analysis')
        response = self.modbus_client.read_input_registers(address=self.current_step_address, count=2, unit=self.control_panel_id)
        step = self._bytes_to_int(response.registers)
        if self.logger:
            self.logger.debug(f'Current chromatograph status: {step}')
        is_ready_for_analysis = step == 4
        if self.logger:
            self.logger.debug(f'Chromatograph is ready for analysis: {is_ready_for_analysis}')
        return is_ready_for_analysis

    def _bytes_to_string(self, response_bytes:list[int]) -> str:
        """
        """
        if self.logger:
            self.logger.debug(f'Converting bytes: {response_bytes} to string')
        string = b''
        for b in response_bytes:
            string += b.to_bytes(2, 'big')
        if self.logger:
            self.logger.log(5, f'String bytes: {string = }')
        string = string.decode().rstrip('\x00')
        if self.logger:
            self.logger.log(5, f'{string = }')
        return string

    def _bytes_to_int(self, response_bytes:list[int]) -> int:
        """
        """
        if self.logger:
            self.logger.debug(f'Converting bytes: {response_bytes} to int')
        integer = response_bytes[0]
        if self.logger:
            self.logger.log(5, f'{integer = }')
        return integer

    def _string_to_bytes(self, string:str) -> tuple[int]:
        """
        """
        if self.logger:
            self.logger.debug(f'Converting string {string} to bytes')
        if len(string) > 30:
            if self.logger:
                self.logger.warning(f'String cannot be > 30 chars long due to modbus limitation. Will be cut to 30 chars')
            string = string[0:30]
        if len(string) % 2 != 0:
            string += '\x00'
        string_bytes = bytes(string.encode())
        if self.logger:
            self.logger.log(5, f'{string_bytes = }')
        message = struct.unpack('>'+'H'*int(len(string_bytes)/2), string_bytes)
        if self.logger:
            self.logger.log(5, f'{message = }')
        return message

    def _double_to_bytes(self, double:float) -> tuple[int]:
        """
        """
        if self.logger:
            self.logger.debug(f'Converting double {double} to bytes')
        double_bytes = struct.pack('<d', double)
        if self.logger:
            self.logger.log(5, f'{double_bytes = }')
        message = struct.unpack('<HHHH', double_bytes)
        if self.logger:
            self.logger.log(5, f'{message = }')
        return message
