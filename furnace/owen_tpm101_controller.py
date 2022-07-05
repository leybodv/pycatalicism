import serial
import time
import threading
import struct

from pycatalicism.furnace.controller import Controller
from pycatalicism.furnace.furnace_data import FurnaceData
from pycatalicism.furnace.furnace_exception import FurnaceException
import pycatalicism.furnace.furnace_logging as logging

class Owen_TPM101_Controller(Controller):
    """
    Class realizes basic functions of TRM101 Owen furnace PID controller using owen protocol (see owen.ru for more details).
    """

    def __init__(self, port:str, baudrate:int, bytesize:int, parity:str, stopbits:float, timeout:float, write_timeout:float|None, rtscts:bool, address:int, rsdl:int, address_len:int):
        """
        Assigns parameters to instance variables, calls __init__ of super class which performs handshake with the device.

        parameters
        ----------
        port:str
            COMM port through which connection with controller is made
        baudrate:int
            Data exchange rate, must match the one at the controller device
        bytesize:int
            Size of byte of information to be sent to the controller
        parity:str
            Whether to control parity
        stopbits:float
            How many stopbits to use when sending information to the device
        timeout:float
            Read timeout in seconds. See pyserial documentation for details (https://pyserial.readthedocs.io/en/latest/pyserial_api.html)
        write_timeout:float|None
            Write timeout in seconds. See pyserial documentation for details (https://pyserial.readthedocs.io/en/latest/pyserial_api.html)
        rtscts:bool
            Enable hardware flow control. See pyserial documentation for details (https://pyserial.readthedocs.io/en/latest/pyserial_api.html)
        address:int
            Address of TRM101 controller, must match the one configured on the device
        rsdl:int
            Time interval in ms between messsage received by the device and receipt sent backwards in response. Must match the one configured on the device
        address_len:int
            Can be set to 8 or 11 bits on the device, however, only 8 bit is supported by this class
        """
        self.logger = logging.get_logger(self.__class__.__name__)
        self.address = address
        self.rsdl = rsdl
        self.address_len = address_len #NB: only 8b adress supported
        self.heating_in_progress = False
        self.port_read_write_lock = threading.Lock()
        self.furnace_data = None
        super().__init__(port=port, baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits, timeout=timeout, write_timeout=write_timeout, rtscts=rtscts)

    def heat(self, temperature:int, wait:int|None) -> FurnaceData|None:
        """
        Heat furnace to specified temperature and wait for specified time in minutes if wait parameter is not None. Method sets SP parameter on the controller to specified temperature. If temperature is 0, r_S parameter is set to StoP value which stops temperature control at TRM101. If temperature is not 0, r_S parameter is set to rUn, thread responsible for current temperature data retreival every 30 seconds is started and method waits until the target temperature is achieved. If wait parameter is not None, sleep for specified time in minutes and turn off controller afterwards.

        parameters
        ----------
        temperature:int
            Target temperature in °C
        wait:int or None
            Time in minutes to hold at target temperature or None if isothermal step is not required

        returns
        -------
        furnace_data:FurnaceData
            Wrapper with time-temperature data
        """
        self._set_SP(value=temperature)
        if temperature == 0:
            self.logger.info('Turning heating off')
            self._set_r_S(value=0)
            self.heating_in_progress = False
            return None
        else:
            self.logger.info(f'Heating furnace to {temperature}°C')
            self._set_r_S(value=1)
            self.heating_in_progress = True
            data_requester = threading.Thread(target=self._request_temperature_data)
            data_requester.start()
            self._wait_until_target_temperature(temperature)
            self.logger.info('Reached target temperature')
            if wait is not None:
                self.logger.info(f'Starting isothermal step for {wait} min')
                time.sleep(wait * 60.0)
                self._finish_isothermal()
                self.logger.info('Finished isothermal step')
            self.heating_in_progress = False
            data_requester.join()
            return self.furnace_data

    def _set_SP(self, value:int):
        """
        Set SP value of the controller. Method prepares parameter change request, sends it to the device and checks receipt

        parameters
        ----------
        value:int
            SP value

        raises
        ------
        FurnaceException
            If wrong receipt was got from device
        """
        command = 'sp'
        message = self._prepare_parameter_change_request(command, value, value_type='PIC')
        with self.port_read_write_lock:
            self._write_message(message)
            receipt = self._read_message()
        if not self._receipt_is_ok(receipt, message):
            raise FurnaceException('Got wrong receipt from device!')

    def _set_r_S(self, value:int):
        """
        Set r_S parameter of the controller. Method prepares parameter change request, sends it to the device and checks receipt

        parameters
        ----------
        value:int
            Value of r_S parameter. Can be 1 (rUn) to turn controller on and 0 (StoP) to turn controller off

        raises
        ------
        FurnaceException
            If wrong receipt was got from device
        """
        command = 'r-s'
        message = self._prepare_parameter_change_request(command, value, value_type='unsigned_byte')
        with self.port_read_write_lock:
            self._write_message(message)
            receipt = self._read_message()
        if not self._receipt_is_ok(receipt=receipt, message=message):
            raise FurnaceException('Got wrong receipt from device!')

    def _request_temperature_data(self):
        """
        Request measured temperature from device every 30 seconds. Method prepares request, gets response, decrypts it into temperature value and makes FurnaceData object with times and temperatures.

        returns
        -------
        furnace_data:FurnaceData
            Wrapper of time-temperature data
        """
        times = []
        temperatures = []
        start_time = time.time()
        command = 'pv'
        message = self._prepare_request(command)
        while self.heating_in_progress:
            response = self._get_response(message)
            temperature = self._get_temperature(response)
            current_time = time.time()
            self.logger.debug(f'Temperature is {temperature} @ {(current_time - start_time) / 60.0} min')
            times.append((current_time - start_time) / 60.0)
            temperatures.append(temperature)
            time.sleep(30)
        self.furnace_data = FurnaceData(times, temperatures)

    def _wait_until_target_temperature(self, temperature:int):
        """
        Wait until measured temperature is reached the target. Method retrieves measured temperature from the device every 10 seconds and terminates when target temperature is achieved.

        parameters
        ----------
        temperature:int
            Target temperature in °C
        """
        command = 'pv'
        message = self._prepare_request(command)
        while self.heating_in_progress:
            response = self._get_response(message)
            measured_temperature = self._get_temperature(response)
            self.logger.debug(f'Temperature is {measured_temperature}°C')
            if measured_temperature >= temperature:
                self.logger.debug('Reached target temperature')
                break
            self.logger.debug('Waiting until target temperature')
            time.sleep(10)

    def _finish_isothermal(self):
        """
        Finish isothermal step. Method sets SP value to 0, r_S value to StoP and heating_in_progress instance variable to False
        """
        self._set_SP(value=0)
        self._set_r_S(value=0)
        self.heating_in_progress = False

    def _prepare_parameter_change_request(self, command:str, value, value_type:str) -> str:
        """
        Method prepares parameter change request to be sent to the device. It gets id of the command, calculates command hash, encrypts value according to specified type and prepares message to send in ASCII format according to owen protocol.

        parameters
        ----------
        command:str
            Command to send to the device, i.e. name of parameter whose value need to be changed
        value
            New value of the parameter. It can have different types depending on the parameter
        value_type:str
            Type of parameter value. Supported types are 'PIC', 'ASCII', which are encrypted according to owen protocol

        returns
        -------
        message_ascii:str
            Message in ASCII format encrypted according to owen protocol

        raises
        ------
        FurnaceException
            If unknown value type is provided
        """
        self.logger.debug(f'Change parameter {command} to {value} of type {value_type}')
        command_id = self._get_command_id(command)
        command_hash = self._get_command_hash(command_id)
        if value_type == 'PIC':
            data = self._float_to_PIC(float(value))
        elif value_type == 'ASCII':
            data = self._str_to_ASCII(str(value))
        elif value_type == 'unsigned_byte':
            data = self._int_to_unsigned_byte(int(value))
        else:
            raise FurnaceException(f'Unknown data type: {value_type}')
        message_ascii = self._get_message_ascii(address=self.address, request=False, data_length=len(data), command_hash=command_hash, data=data)
        return message_ascii

    def _get_temperature(self, response:str) -> float:
        """
        Decrypt recieved message, check CRC and retrieve temperature value.

        parameters
        ----------
        response:str
            Tetrad-to-ASCII encrypted according to owen protocol message received from the device

        returns
        -------
        temperature:float
            Temperature value measured by the device in °C

        raises
        ------
        FurnaceException
            If CRC check sum is incorrect
        """
        address, flag_byte, response_hash, data, crc = self._unpack_message(response)
        if not self._crc_is_ok(address, flag_byte, response_hash, data, crc):
            raise FurnaceException('Wrong CRC in response message!')
        temperature = self._decrypt_PIC(data)
        return temperature

    def _float_to_PIC(self, value:float) -> list[int]:
        """
        Encrypt float value to PIC bytes according to owen protocol

        parameters
        ----------
        value:float
            Value to encrypt

        returns
        -------
        pic_bytes:list[int]
            List of 3 bytes of encrypted value
        """
        pic_bytes = []
        ieee = struct.pack('>f', value)
        self.logger.log(5, f'{[b for b in ieee] = }')
        for i in range(3):
            pic_bytes.append(ieee[i])
        self.logger.debug(f'{pic_bytes = }')
        return pic_bytes

    def _int_to_unsigned_byte(self, value:int) -> list[int]:
        """
        """
        if value > 255 or value < 0:
            raise FurnaceException(f'Got wrong value to convert to unsigned byte: {value}')
        unsigned_bytes = [value]
        self.logger.debug(f'{unsigned_bytes = }')
        return unsigned_bytes

    def _str_to_ASCII(self, value:str) -> list[int]:
        """
        Encrypt string value to ASCII bytes according to owen protocol

        parameters
        ----------
        value:str
            String to be encrypted and sent to the device according to owen protocol

        returns
        -------
            List of ASCII bytes to be sent to the device

        raises
        ------
        FurnaceException
            If non-ASCII character was encountered in the value
        """
        ascii_bytes = []
        for ch in value[::-1]:
            if ord(ch) > 127:
                raise FurnaceException(f'Non ASCII character was met in value: {ch}')
            ascii_bytes.append(ord(ch))
        return ascii_bytes

    def _decrypt_PIC(self, data:list[int]|None) -> float:
        """
        Decrypt float value from PIC bytes received from the device

        parameters
        ----------
        data:list[int]
            List of 3 bytes received from the device

        returns
        -------
        pic:float
            Float value decrypted according to owen protocol

        raises
        ------
        FurnaceException
            If data is None or if size of data list is greater than 3 bytes
        """
        if data is None:
            raise FurnaceException('Cannot decrypt empty data')
        if len(data) > 3:
            raise FurnaceException('Unexpected size of data to convert to PIC float')
        data_str = b''
        for b in data:
            data_str = data_str + b.to_bytes(1, 'big')
        data_str = data_str + int(0).to_bytes(1, 'big')
        pic = struct.unpack('>f', data_str)[0]
        return pic

    def handshake(self) -> bool:
        """
        Performs handshake with the device. Method sends 'dev' command to the device and checks if it returns expected value corresponding to the device name.

        returns
        -------
        success:bool
            True if device name is ТРМ101
        """
        self.logger.info('Handshaking with the controller')
        command = 'dev'
        message = self._prepare_request(command)
        response = self._get_response(message)
        device_name = self._get_device_name(response)
        self.logger.debug(f'{device_name = }')
        # return device_name == 'ТРМ101' #NB: <- this is utf-8 string written in russian, so ascii answer can be different, check ASCII codes!!!
        return device_name == 'ÒÐÌ101' # <- this string is actually returned by the device \_O_/

    def _prepare_request(self, command:str) -> str:
        """
        Prepares request of parameter value in tetrad-to-ASCII form according to owen protocol. Methods gets command id, retreives command hash and encrypts message.

        parameters
        ----------
        command:str
            Parameter name to get value of from the device

        returns
        -------
        message_ascii:str
            Encrypted in tetrad-to-ASCII form according to owen protocol message to be sent to the device
        """
        self.logger.debug(f'Request {command} parameter value from device')
        command_id = self._get_command_id(command)
        command_hash = self._get_command_hash(command_id)
        message_ascii = self._get_message_ascii(address=self.address, request=True, data_length=0, command_hash=command_hash, data=None)
        return message_ascii

    def _get_response(self, message:str) -> str:
        """
        Writes message to the device, gets receipt and checks it and, finally, gets a response from the device.

        parameters
        ----------
        message:str
            Message encrypted in tetrad-to-ASCII form according to owen protocol to be sent to the device.

        returns
        -------
        response:str
            Message received from the device encrypted in tetrad-to-ASCII from according to owen protocol.

        raises
        ------
        FurnaceException
            If receipt is wrong
        """
        with self.port_read_write_lock:
            self._write_message(message)
            # receipt = self._read_message()
            # if not self._receipt_is_ok(receipt, message):
                # raise FurnaceException(f'Got wrong receipt from device!')
            response = self._read_message()
        return response

    def _get_device_name(self, response:str) -> str:
        """
        Decrypts response received from the device in tetrad-to-ASCII form, checks CRC and retreives device name.

        parameters
        ----------
        response:str
            Response received from the device encrypted in tetrad-to-ASCII form according owen protocol.

        returns
        -------
        device_name:str
            Name of the device

        raises
        ------
        FurnaceException
            If CRC check sum is not correct
        """
        address, flag_byte, response_hash, data, crc = self._unpack_message(response)
        if not self._crc_is_ok(address, flag_byte, response_hash, data, crc):
            raise FurnaceException(f'Wrong CRC in response message!')
        device_name = self._decrypt_string(data)
        return device_name

    def _get_command_id(self, command:str) -> list[int]:
        """
        Encrypt command name to command id according to owen protocol.

        parameters
        ----------
        command:str
            String representation of command

        returns
        -------
        command_id:list[int]
            List of 4 bytes representing encrypted command id according to owen protocol

        raises
        ------
        FurnaceException
            If illegal char encountered in command name or if command id has more than 4 bytes
        """
        command_id = []
        command_cap = command.upper()
        for i in range(len(command_cap)):
            if command_cap[i] == '.':
                continue
            elif command_cap[i].isdecimal():
                ch_id = ord(command_cap[i]) - ord('0')
            elif command_cap[i].isalpha():
                ch_id = ord(command_cap[i]) - ord('A') + 10
            elif command_cap[i] == '-':
                ch_id = 36
            elif command_cap[i] == '_':
                ch_id = 37
            elif command_cap[i] == '/':
                ch_id = 38
            else:
                raise FurnaceException(f'Illegal char in command name: {command_cap[i]}')
            ch_id = ch_id * 2
            if i < len(command_cap) - 1 and command_cap[i+1] == '.':
                ch_id = ch_id + 1
            command_id.append(ch_id)
        if len(command_id) > 4:
            raise FurnaceException('Command ID cannot contain more than 4 characters!')
        if len(command_id) < 4:
            for i in range(4 - len(command_id)):
                command_id.append(78)
        return command_id

    def _get_command_hash(self, command_id:list[int]) -> int:
        """
        Calculates 2 bytes command hash according to owen protocol.

        parameters
        ----------
        command_id:list[int]
            List of 4 bytes encrypted command id

        returns
        -------
        command_hash:int
            2 bytes command hash
        """
        command_hash = 0
        for b in command_id:
            b = b << 1
            b = b & 0xff
            for i in range(7):
                if (b ^ (command_hash >> 8)) & 0x80:
                    command_hash = command_hash << 1
                    command_hash = command_hash ^ 0x8f57
                else:
                    command_hash = command_hash << 1
                command_hash = command_hash & 0xffff
                b = b << 1
                b = b & 0xff
        self.logger.log(5, f'{command_hash = :#x}')
        return command_hash

    def _get_crc(self, message_bytes:list[int]) -> int:
        """
        Calculate CRC check sum for message according to owen protocol.

        parameters
        ----------
        message_bytes:list[int]
            Message bytes containing address byte, flag byte, hash bytes and data bytes encrypted according owen protocol.

        returns
        -------
        crc:int
            2 bytes CRC chack sum according owen protocol.
        """
        crc = 0
        for b in message_bytes:
            b = b & 0xff
            for i in range(8):
                if (b ^ (crc >> 8)) & 0x80:
                    crc = crc << 1
                    crc = crc ^ 0x8f57
                else:
                    crc = crc << 1
                crc = crc & 0xffff
                b = b << 1
                b = b & 0xff
        return crc

    def _get_message_ascii(self, address:int, request:bool, data_length:int, command_hash:int, data:list[int]|None) -> str:
        """
        Encrypt message in tetrad-to-ASCII form according to owen protocol.

        parameters
        ----------
        address:int
            Byte with address of the device. Must match the one configured on the device.
        request:bool
            True if message contains request of parameter value.
        data_length:int
            Number of bytes used to encrypt data. Must be in range [0,15]
        command_hash:int
            2 bytes encrypted according to owen protocol command hash.
        data:list[int] or None
            Data to be sent to the device encrypted as byte list according to the owen protocol or None if no data is sent to the device

        returns
        -------
        message:str
            tetrad-to-ASCII encrypted according to owen protocol message

        raises
        ------
        FurnaceException
            If data length is larger 15 or data_length parameter does not match length of data bytes list or if encrypted message contains wrong characters
        """
        if data_length > 15:
            raise FurnaceException('Data length cannot be larger than 15')
        if data is None and data_length != 0:
            raise FurnaceException('data_length parameter cannot be non zero if data is None')
        message_bytes = []
        message_bytes.append(address & 0xff)
        # NB: if address_len is 11b flag_byte must be modified accordingly
        flag_byte = 0
        if request:
            flag_byte = flag_byte | 0b00010000
        flag_byte = flag_byte | data_length
        message_bytes.append(flag_byte & 0xff)
        message_bytes.append((command_hash >> 8) & 0xff)
        message_bytes.append(command_hash & 0xff)
        if data is not None:
            if len(data) > 15:
                raise FurnaceException('Data length cannot be larger than 15')
            if len(data) != data_length:
                raise FurnaceException('Length of data bytes list does not match data_length parameter')
            for data_byte in data:
                message_bytes.append(data_byte & 0xff)
        crc = self._get_crc(message_bytes)
        message_bytes.append((crc >> 8) & 0xff)
        message_bytes.append(crc & 0xff)
        message = chr(0x23)
        for byte in message_bytes:
            message = message + chr(((byte >> 4) & 0xf) + 0x47)
            message = message + chr((byte & 0xf) + 0x47)
        message = message + chr(0x0d)
        for ch in message:
            if ch not in ['#', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', '\r']:
                raise FurnaceException(f'Wrong ASCII message: "{message}"!')
        return message

    def _write_message(self, message:str):
        """
        Writes enctypted message over serial port. Waits rsdl ms to give time for the device to send receipt back.

        parameters
        ----------
        message:str
            Encrypted message to be sent to the device
        """
        with serial.Serial(port=self.port, baudrate=self.baudrate, bytesize=self.bytesize, parity=self.parity, stopbits=self.stopbits, timeout=self.timeout, rtscts=self.rtscts, write_timeout=self.write_timeout) as ser:
            self.logger.debug(f'Writing message: {bytes(message, encoding="ascii")}')
            ser.write(bytes(message, encoding='ascii'))

    def _read_message(self) -> str:
        """
        Reads message from the device over serial port.

        returns
        -------
        message:str
            Encrypted message received from the device

        raises
        ------
        FurnaceException
            If message does not contain proper start and stop markers
        """
        with serial.Serial(port=self.port, baudrate=self.baudrate, bytesize=self.bytesize, parity=self.parity, stopbits=self.stopbits, timeout=self.timeout, rtscts=self.rtscts, write_timeout=self.write_timeout) as ser:
            message = ''
            for i in range(44):
                self.logger.log(5, f'Reading byte #{i}')
                byte = ser.read().decode()
                self.logger.log(5, f'Read byte: {byte}')
                message = message + byte
                if byte == chr(0x0d):
                    break
            self.logger.debug(f'Got message: {message = }')
        if message[0] != chr(0x23) or message[-1] != chr(0x0d):
            raise FurnaceException(f'Unexpected format of message got from device: {message}')
        return message

    def _receipt_is_ok(self, receipt:str, message:str) -> bool:
        """
        Checks whether receipt received from the device is correct.

        parameters
        ----------
        receipt:str
            Receipt message received from the device in enctypted form
        message:str
            Message that was sent to the device in enctypted form

        returns
        -------
        receipt_is_ok:bool
            True if receipt is correct
        """
        address, flag_byte, response_hash, data, crc = self._unpack_message(receipt)
        self.logger.log(5, f'Receipt address: {address}')
        self.logger.log(5, f'Receipt flag_byte: {flag_byte:#b}')
        self.logger.log(5, f'Receipt response_hash: {response_hash:#x}')
        self.logger.log(5, f'Receipt data: {data}')
        self.logger.log(5, f'Receipt crc: {crc}')
        self.logger.log(5, f'Receipt crc is ok: {self._crc_is_ok(address, flag_byte, response_hash, data, crc)}')
        new_flag_tetrad = (ord(message[3]) - 0x47) & 0b1110
        new_flag_chr = chr((new_flag_tetrad & 0xf) + 0x47)
        message_without_request = ''
        for i in range(len(message)):
            if i == 3:
                message_without_request = message_without_request + new_flag_chr
            else:
                message_without_request = message_without_request + message[i]
        receipt_is_ok = message_without_request == receipt
        self.logger.debug(f'Receipt is ok: {receipt_is_ok}')
        return receipt_is_ok

    def _crc_is_ok(self, address:int, flag_byte:int, response_hash:int, data:list[int]|None, crc_to_check:int) -> bool:
        """
        Checks CRC check sum of received message.

        parameters
        ----------
        address:int
            Address byte
        flag_byte:int
            Flag byte
        response_hash:int
            2 byte response command hash
        data:list[int] or None
            List of bytes with enctypted data or None if data bytes were empty
        crc_to_check:int
            2 bytes CRC check sum that was received in the message

        returns
        -------
        crc_is_ok:bool
            True if CRC check sum is correct
        """
        message_bytes = []
        message_bytes.append(address)
        message_bytes.append(flag_byte)
        message_bytes.append((response_hash >> 8) & 0xff)
        message_bytes.append(response_hash & 0xff)
        if data is not None:
            for data_byte in data:
                message_bytes.append(data_byte & 0xff)
        crc = self._get_crc(message_bytes)
        crc_is_ok = crc == crc_to_check
        self.logger.debug(f'{crc_is_ok = }')
        return crc_is_ok

    def _decrypt_string(self, data:list[int]|None) -> str:
        """
        Decrypt string message from data bytes received from the device.

        parameters
        ----------
        data:list[int]
            List of bytes with encrypted string value

        returns
        -------
        string:str
            Decrypted string value

        raises
        ------
        FurnaceException
            If data is None
        """
        self.logger.debug(f'{data = }')
        if data is None:
            raise FurnaceException('Cannot decrypt empty data!')
        string = ''
        for data_byte in data[::-1]:
            string = string + chr(data_byte)
        return string

    def _unpack_message(self, message:str) -> tuple[int, int, int, list[int]|None, int]:
        """
        Decrypt tetrad-to-ASCII encrypted message according to owen protocol into bytes.

        parameters
        ----------
        message:str
            Tetrad-to-ASCII encrypted message received from the device

        returns
        -------
        address:int
            Byte with address parameter
        flag_byte:int
            Byte with enhanced address, request and data length bits
        response_hash:int
            2 bytes hash of command id
        data:list[int] or None
            List of bytes with data encrypted according to owen protocol or None if data length is 0
        crc:int
            2 bytes CRC check sum received in message

        raises
        ------
        FurnaceException
            If received message does not contain proper start and stop markers
        """
        if message[0] != chr(0x23) or message[-1] != chr(0x0d):
            raise FurnaceException(f'Unexpected format of message from device: {message}')
        message_bytes = []
        for i in range(1, len(message) - 1, 2):
            first_tetrad = (ord(message[i]) - 0x47) & 0xf
            second_tetrad = (ord(message[i+1]) - 0x47) & 0xf
            self.logger.log(5, f'ASCII letter #{i} = {message[i]}')
            self.logger.log(5, f'{first_tetrad = :#b}')
            self.logger.log(5, f'{second_tetrad = :#b}')
            byte = ((first_tetrad << 4) | second_tetrad) & 0xff
            message_bytes.append(byte)
        self.logger.log(5, f'{len(message_bytes) = }')
        self.logger.log(5, f'{message_bytes = }')
        address = message_bytes[0]
        self.logger.log(5, f'{address = }')
        flag_byte = message_bytes[1]
        self.logger.log(5, f'{flag_byte = :#b}')
        response_hash = ((message_bytes[2] << 8) | message_bytes[3]) & 0xffff
        self.logger.log(5, f'{response_hash = :#x}')
        data_length = flag_byte & 0b1111
        self.logger.log(5, f'{data_length = }')
        if data_length != 0:
            data = []
            for i in range(data_length):
                data.append(message_bytes[4 + i])
        else:
            data = None
        crc = ((message_bytes[4+data_length] << 8) | message_bytes[4+data_length+1]) & 0xffff
        return (address, flag_byte, response_hash, data, crc)
