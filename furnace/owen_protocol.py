import threading
import serial
import struct

import pycatalicism.furnace.furnace_logging as furnace_logging
from pycatalicism.furnace.furnace_exceptions import FurnaceProtocolException
from pycatalicism.furnace.furnace_exceptions import FurnaceConnectionException

class OwenProtocol():
    """
    """

    def __init__(self, address:int, port:str, baudrate:int, bytesize:int, parity:str, stopbits:float, timeout:float, write_timeout:float|None, rtscts:bool, request_trials:int=3):
        """
        TODO: add request trials
        """
        self._address = address
        self._port = port
        self._baudrate = baudrate
        self._bytesize = bytesize
        self._parity = parity
        self._stopbits = stopbits
        self._timeout = timeout
        self._rtscts = rtscts
        self._write_timeout = write_timeout
        self._read_write_lock = threading.Lock()
        self._request_trials = request_trials
        self._logger = furnace_logging.get_logger(self.__class__.__name__)

    ## Public interface ##

    def request_string(self, parameter:str) -> str:
        """
        """
        message = self._pack_message(command=parameter, is_request=True, data=None)
        count = 0
        while True:
            self._logger.debug(f'Requesting string parameter "{parameter}". Trial #{count}.')
            try:
                parameter_data_bytes = self._get_parameter_data_bytes(message=message)
                self._logger.log(5, f'{parameter_data_bytes = }')
                string = self._decrypt_string(parameter_data_bytes)
                self._logger.log(5, f'{string = }')
                break
            except FurnaceProtocolException as ex:
                if count == self._request_trials-1:
                    raise FurnaceConnectionException(ex)
                else:
                    count += 1
        return string

    def request_PIC(self, parameter:str) -> float:
        """
        """
        message = self._pack_message(command=parameter, is_request=True, data=None)
        count = 0
        while True:
            self._logger.debug(f'Requesting PIC parameter "{parameter}". Trial #{count}.')
            try:
                parameter_data_bytes = self._get_parameter_data_bytes(message)
                self._logger.log(5, f'{parameter_data_bytes = }')
                pic = self._decrypt_PIC(parameter_data_bytes)
                self._logger.log(5, f'{pic = }')
                break
            except FurnaceProtocolException as ex:
                if count == self._request_trials-1:
                    raise FurnaceConnectionException(ex)
                else:
                    count += 1
        return pic

    def send_PIC(self, parameter:str, value:float):
        """
        """
        data = self._float_to_PIC(value=value)
        message = self._pack_message(command=parameter, is_request=False, data=data)
        count = 0
        while True:
            self._logger.debug(f'Sending PIC parameter "{parameter}". Trial #{count}.')
            try:
                self._change_parameter_value(message=message)
                break
            except FurnaceProtocolException as ex:
                if count == self._request_trials-1:
                    raise FurnaceConnectionException(ex)
                else:
                    count += 1

    def send_unsigned_byte(self, parameter:str, value:int):
        """
        """
        data = self._int_to_unsigned_byte(value=value)
        message = self._pack_message(command=parameter, is_request=False, data=data)
        count = 0
        while True:
            self._logger.debug(f'Sending unsigned byte parameter "{parameter}". Trial #{count}.')
            try:
                self._change_parameter_value(message=message)
                break
            except FurnaceProtocolException as ex:
                if count == self._request_trials-1:
                    raise FurnaceConnectionException(ex)
                else:
                    count += 1

    ## Top level i/o ##

    def _change_parameter_value(self, message:str):
        """
        """
        with self._read_write_lock:
            self._write_message(message)
            receipt = self._read_message()
        if not self._receipt_is_ok(receipt=receipt, message=message):
            raise FurnaceProtocolException('Got wrong receipt from device!')

    def _get_parameter_data_bytes(self, message:str) -> list[int]:
        """
        TODO: Change docs
        Writes message to the device and gets a response from the device.

        parameters
        ----------
        message:str
            Message encrypted in tetrad-to-ASCII form according to owen protocol to be sent to the device.

        returns
        -------
        response:str
            Message received from the device encrypted in tetrad-to-ASCII from according to owen protocol.
        """
        with self._read_write_lock:
            self._write_message(message)
            response = self._read_message()
        address, flag_byte, response_hash, data, crc = self._unpack_message(response)
        if not self._crc_is_ok(address, flag_byte, response_hash, data, crc):
            raise FurnaceProtocolException(f'Wrong CRC in response message!')
        if data is None:
            raise FurnaceProtocolException('Did not get any data in response message')
        return data

    ## Bottom level i/o ##

    def _write_message(self, message:str):
        """
        Writes enctypted message over serial port.

        parameters
        ----------
        message:str
            Encrypted message to be sent to the device
        """
        with serial.Serial(port=self._port, baudrate=self._baudrate, bytesize=self._bytesize, parity=self._parity, stopbits=self._stopbits, timeout=self._timeout, rtscts=self._rtscts, write_timeout=self._write_timeout) as ser:
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
        with serial.Serial(port=self._port, baudrate=self._baudrate, bytesize=self._bytesize, parity=self._parity, stopbits=self._stopbits, timeout=self._timeout, rtscts=self._rtscts, write_timeout=self._write_timeout) as ser:
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
            raise FurnaceProtocolException(f'Unexpected format of message got from device: {message}')
        return message

    ## Encrypt data to bytes ##

    def _float_to_PIC(self, value:float) -> list[int]:
        """
        Encrypt float value to PIC bytes according to owen protocol. Encrypted bytes can be sent in data block of the message.

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
        Encrypt int value to unsigned byte according to owen protocol. Encrypted bytes can be sent in data block of the message

        parameters
        ----------
        value:int
            value to convert to byte

        returns
        -------
        unsigned_byte:list[int]
            list of 1 byte with converted value

        raises
        ------
        FurnaceException
            if value > 255 or value < 0
        """
        if value > 255 or value < 0:
            raise FurnaceProtocolException(f'Got wrong value to convert to unsigned byte: {value}')
        unsigned_bytes = [value]
        self.logger.debug(f'{unsigned_bytes = }')
        return unsigned_bytes

    def _str_to_ASCII(self, value:str) -> list[int]:
        """
        Encrypt string value to ASCII bytes according to owen protocol. Encrypted bytes can be sent in data block of the message.

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
                raise FurnaceProtocolException(f'Non ASCII character was met in value: {ch}')
            ascii_bytes.append(ord(ch))
        return ascii_bytes

    ## Decrypt data from bytes ##

    def _decrypt_PIC(self, data:list[int]) -> float:
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
            raise FurnaceProtocolException('Cannot decrypt empty data')
        if len(data) > 3:
            raise FurnaceProtocolException('Unexpected size of data to convert to PIC float')
        data_str = b''
        for b in data:
            data_str = data_str + b.to_bytes(1, 'big')
        data_str = data_str + int(0).to_bytes(1, 'big')
        pic = struct.unpack('>f', data_str)[0]
        return pic

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
            raise FurnaceProtocolException('Cannot decrypt empty data!')
        string = ''
        for data_byte in data[::-1]:
            string = string + chr(data_byte)
        return string

    ## Message packing/unpacking ##

    def _pack_message(self, command:str, is_request:bool, data:list[int]|None) -> str:
        """
        TODO: change docs
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
        data_length = 0 if data is None else len(data)
        message_ascii = self._encrypt_tetrad_to_ascii(address=self._address, request=is_request, data_length=data_length, command_hash=command_hash, data=data)
        return message_ascii

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
                raise FurnaceProtocolException(f'Illegal char in command name: {command_cap[i]}')
            ch_id = ch_id * 2
            if i < len(command_cap) - 1 and command_cap[i+1] == '.':
                ch_id = ch_id + 1
            command_id.append(ch_id)
        if len(command_id) > 4:
            raise FurnaceProtocolException('Command ID cannot contain more than 4 characters!')
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

    def _encrypt_tetrad_to_ascii(self, address:int, request:bool, data_length:int, command_hash:int, data:list[int]|None) -> str:
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
            raise FurnaceProtocolException('Data length cannot be larger than 15')
        if data is None and data_length != 0:
            raise FurnaceProtocolException('data_length parameter cannot be non zero if data is None')
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
                raise FurnaceProtocolException('Data length cannot be larger than 15')
            if len(data) != data_length:
                raise FurnaceProtocolException('Length of data bytes list does not match data_length parameter')
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
                raise FurnaceProtocolException(f'Wrong ASCII message: "{message}"!')
        return message

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
            raise FurnaceProtocolException(f'Unexpected format of message from device: {message}')
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

    ## Checking ##

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
