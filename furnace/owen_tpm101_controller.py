import serial

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
        receipt = self._read_message(read_timeout=50)
        if not self._receipt_is_ok(receipt, message):
            raise FurnaceException(f'Got wrong receipt from device!')
        response = self._read_message(read_timeout=0)
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
        raise NotImplementedError()

    def _get_message_ascii(self, address:int, request:bool, data_length:int, command_hash:int, data:None) -> str:
        """
        """
        raise NotImplementedError()

    def _write_message(self, message:str):
        """
        """
        raise NotImplementedError()

    def _read_message(self, read_timeout) -> str:
        """
        """
        raise NotImplementedError()

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

    def _unpack_message(self, message:str):
        """
        """
        raise NotImplementedError()
