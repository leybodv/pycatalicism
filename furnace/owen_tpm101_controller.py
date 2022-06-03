import serial
import time

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

    def heat(self, temperature:int, wait:int|None) -> FurnaceData:
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
        _, address, flag_byte, response_hash, data, crc = self._unpack_message(response)
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

    def _get_message_ascii(self, address:int, request:bool, data_length:int, command_hash:int, data:None) -> str:
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
            for i in range(data_length):
                message_bytes.append((data >> data_length - i - 1) & 0xff)
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
        with serial.Serial(port=self.port, baudrate=self.baudrate, bytesize=self.bytesize, parity=self.parity, stopbits=self.stopbits, timeout=self.timeout, rtscts=self.rtscts, write_timeout=self.write_timeout) as ser:
            ser.write(message)
        time.sleep(self.rsdl / 1000)

    def _read_message(self) -> str:
        """
        """
        with serial.Serial(port=self.port, baudrate=self.baudrate, bytesize=self.bytesize, parity=self.parity, stopbits=self.stopbits, timeout=self.timeout, rtscts=self.rtscts, write_timeout=self.write_timeout) as ser:
            message = ser.read_until(expected=chr(0x0d)).decode()
        if message[0] != chr(0x23) or message[-1] != chr(0x0d):
            raise FurnaceException(f'Unexpected format of message got from device: {message}')
        return message

    def _receipt_is_ok(self, receipt:str, message:str) -> bool:
        """
        """
        raise NotImplementedError()

    def _crc_is_ok(self, address:int, flag_byte:int, response_hash:int, data:int, crc:int) -> bool:
        """
        """
        raise NotImplementedError()

    def _decrypt_string(self, data:int) -> str:
        """
        """
        raise NotImplementedError()

    def _unpack_message(self, message:str) -> tuple[int, int, int, int, int, int]:
        """
        """
        raise NotImplementedError()
