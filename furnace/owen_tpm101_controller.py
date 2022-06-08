import serial
import time
import threading

from pycatalicism.furnace.controller import Controller
from pycatalicism.furnace.furnace_data import FurnaceData
from pycatalicism.furnace.furnace_exception import FurnaceException

class Owen_TPM101_Controller(Controller):
    """
    """

    def __init__(self, port:str, baudrate:int, bytesize:int, parity:str, stopbits:float, timeout:float, write_timeout:float, rtscts:bool, address:int, rsdl:int, address_len:int):
        """
        """
        super().__init__(port=port, baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits, timeout=timeout, write_timeout=write_timeout, rtscts=rtscts)
        self.address = address
        self.rsdl = rsdl
        self.address_len = address_len #NB: only 8b adress supported
        self.heating_in_progress = False
        self.port_read_write_lock = threading.Lock()
        self.furnace_data = None

    def heat(self, temperature:int, wait:int|None) -> FurnaceData|None:
        """
        """
        self._set_SP(value=temperature)
        if temperature == 0:
            self._set_r_S(value='STOP')
            self.heating_in_progress = False
            return None
        else:
            self._set_r_S(value='RUN')
            self.heating_in_progress = True
            data_requester = threading.Thread(target=self._request_temperature_data)
            data_requester.start()
            self._wait_until_target_temperature(temperature)
            if wait is not None:
                timer = threading.Timer(wait * 60, self._finish_isothermal)
                timer.start()
                timer.join()
            self.heating_in_progress = False
            data_requester.join()
            return self.furnace_data

    def _set_SP(self, value:int):
        """
        """
        command = 'sp'
        message = self._prepare_parameter_change_request(command, value, value_type='PIC')
        self._write_message(message)
        receipt = self._read_message()
        if not self._receipt_is_ok(receipt, message):
            raise FurnaceException('Got wrong receipt from device!')

    def _set_r_S(self, value:str):
        """
        """
        command = 'r-s'
        message = self._prepare_parameter_change_request(command, value, value_type='ASCII')
        self._write_message(message)
        receipt = self._read_message()
        if not self._receipt_is_ok(receipt=receipt, message=message):
            raise FurnaceException('Got wrong receipt from device!')

    def _request_temperature_data(self):
        """
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
            times.append((current_time - start_time) / 60.0)
            temperatures.append(temperature)
            time.sleep(30)
        self.furnace_data = FurnaceData(times, temperatures)

    def _wait_until_target_temperature(self, temperature:int):
        """
        """
        command = 'pv'
        message = self._prepare_request(command)
        while self.heating_in_progress:
            response = self._get_response(message)
            measured_temperature = self._get_temperature(response)
            if abs((temperature - measured_temperature) / temperature) < 0.05:
                break
            time.sleep(10)

    def _finish_isothermal(self):
        """
        """
        self._set_SP(value=0)
        self._set_r_S(value='STOP')
        self.heating_in_progress = False

    def _prepare_parameter_change_request(self, command:str, value, value_type:str) -> str:
        """
        """
        raise NotImplementedError()

    def _get_temperature(self, response:str) -> float:
        """
        """
        raise NotImplementedError()

    def _handshake(self) -> bool:
        """
        """
        command = 'dev'
        message = self._prepare_request(command)
        response = self._get_response(message)
        device_name = self._get_device_name(response)
        return device_name == 'ТРМ101' #NB: <- this is utf-8 string written in russian, so ascii answer can be different, check ASCII codes!!!

    def _prepare_request(self, command:str) -> str:
        """
        """
        command_id = self._get_command_id(command)
        command_hash = self._get_command_hash(command_id)
        message_ascii = self._get_message_ascii(address=self.address, request=True, data_length=0, command_hash=command_hash, data=None)
        return message_ascii

    def _get_response(self, message:str) -> str:
        """
        """
        self._write_message(message)
        receipt = self._read_message()
        if not self._receipt_is_ok(receipt, message):
            raise FurnaceException(f'Got wrong receipt from device!')
        response = self._read_message()
        return response

    def _get_device_name(self, response:str) -> str:
        """
        """
        address, flag_byte, response_hash, data, crc = self._unpack_message(response)
        if not self._crc_is_ok(address, flag_byte, response_hash, data, crc):
            raise FurnaceException(f'Wrong CRC in response message!')
        device_name = self._decrypt_string(data)
        return device_name

    def _get_command_id(self, command:str) -> list[int]:
        """
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
        return command_hash

    def _get_crc(self, message_bytes:list[int]) -> int:
        """
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
        """
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
        """
        with self.port_read_write_lock:
            with serial.Serial(port=self.port, baudrate=self.baudrate, bytesize=self.bytesize, parity=self.parity, stopbits=self.stopbits, timeout=self.timeout, rtscts=self.rtscts, write_timeout=self.write_timeout) as ser:
                ser.write(message)
            time.sleep(self.rsdl / 1000)

    def _read_message(self) -> str:
        """
        """
        with self.port_read_write_lock:
            with serial.Serial(port=self.port, baudrate=self.baudrate, bytesize=self.bytesize, parity=self.parity, stopbits=self.stopbits, timeout=self.timeout, rtscts=self.rtscts, write_timeout=self.write_timeout) as ser:
                message = ser.read_until(expected=chr(0x0d)).decode()
            if message[0] != chr(0x23) or message[-1] != chr(0x0d):
                raise FurnaceException(f'Unexpected format of message got from device: {message}')
            return message

    def _receipt_is_ok(self, receipt:str, message:str) -> bool:
        """
        """
        new_flag_tetrad = (ord(message[3]) - 0x47) & 0b1110
        new_flag_chr = chr((new_flag_tetrad & 0xf) + 0x47)
        message_without_request = ''
        for i in range(len(message)):
            if i == 3:
                message_without_request = message_without_request + new_flag_chr
            else:
                message_without_request = message_without_request + message[i]
        receipt_is_ok = message_without_request == receipt
        return receipt_is_ok

    def _crc_is_ok(self, address:int, flag_byte:int, response_hash:int, data:list[int]|None, crc_to_check:int) -> bool:
        """
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
        return crc_is_ok

    def _decrypt_string(self, data:list[int]|None) -> str:
        """
        """
        if data is None:
            raise FurnaceException('Cannot decrypt empty data!')
        string = ''
        for data_byte in data:
            string = string + chr(data_byte)
        return string

    def _unpack_message(self, message:str) -> tuple[int, int, int, list[int]|None, int]:
        """
        """
        if message[0] != chr(0x23) or message[-1] != chr(0x0d):
            raise FurnaceException(f'Unexpected format of message from device: {message}')
        message_bytes = []
        for i in range(1, len(message) - 1, 2):
            first_tetrad = (ord(message[i]) - 0x47) & 0xf
            second_tetrad = (ord(message[i+1]) - 0x47) & 0xf
            byte = ((first_tetrad << 4) | second_tetrad) & 0xff
            message_bytes.append(byte)
        address = message_bytes[0]
        flag_byte = message_bytes[1]
        response_hash = ((message_bytes[2] << 8) | message_bytes[3]) & 0xffff
        data_length = flag_byte | 0b1111
        if data_length != 0:
            data = []
            for i in range(data_length):
                data.append(message_bytes[4 + i])
        else:
            data = None
        crc = ((message_bytes[4+data_length] << 8) | message_bytes[4+data_length+1]) & 0xffff
        return (address, flag_byte, response_hash, data, crc)
