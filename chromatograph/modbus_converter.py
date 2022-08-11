import struct

import pycatalicism.chromatograph.chromatograph_logging as chromatograph_logging

_logger = chromatograph_logging.get_logger(__name__)

def bytes_to_string(response_bytes:list[int]) -> str:
    """
    Converts bytes received from chromatograph to string.

    parameters
    ----------
    response_bytes:list[int]
        bytes received from chromatograph

    returns
    -------
    string:str
        decoded string
    """
    _logger.debug(f'Converting bytes: {response_bytes} to string')
    string = b''
    for b in response_bytes:
        string += b.to_bytes(2, 'big')
    _logger.log(5, f'String bytes: {string = }')
    string = string.decode().rstrip('\x00')
    _logger.log(5, f'{string = }')
    return string

def bytes_to_int(response_bytes:list[int]) -> int:
    """
    Converts bytes received from chromatograph to integer.

    parameters
    ----------
    response_bytes:list[int]
        bytes received from chromatograph

    returns
    -------
    integer:int
        decoded integer
    """
    _logger.debug(f'Converting bytes: {response_bytes} to int')
    integer = response_bytes[0]
    _logger.log(5, f'{integer = }')
    return integer

def string_to_bytes(string:str) -> tuple[int]:
    """
    Encodes string into bytes to be sent to chromatograph. NB: if string is more than 30 chars long, it will be concatenated to 30 chars due to the modbus limitations. A warning is logged in this case.

    parameters
    ----------
    string:str
        string to encode

    returns
    -------
    message:tuple[int]
        bytes to sent to chromatograph
    """
    _logger.debug(f'Converting string {string} to bytes')
    if len(string) > 30:
        _logger.warning(f'String cannot be > 30 chars long due to modbus limitation. Will be cut to 30 chars')
        string = string[0:30]
    if len(string) % 2 != 0:
        string += '\x00'
    string_bytes = bytes(string.encode())
    _logger.log(5, f'{string_bytes = }')
    message = struct.unpack('>'+'H'*int(len(string_bytes)/2), string_bytes)
    _logger.log(5, f'{message = }')
    return message

def double_to_bytes(double:float) -> tuple[int]:
    """
    Encodes double value into bytes to be sent to chromatograph.

    parameters
    ----------
    double:float
        value to encode

    returns
    -------
    message:tuple[int]
        bytes to sent to chromatograph
    """
    _logger.debug(f'Converting double {double} to bytes')
    double_bytes = struct.pack('<d', double)
    _logger.log(5, f'{double_bytes = }')
    message = struct.unpack('<HHHH', double_bytes)
    _logger.log(5, f'{message = }')
    return message
