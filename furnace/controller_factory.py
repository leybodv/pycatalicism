"""
Module is a factory of concrete controller classes to use in a program
"""

from pycatalicism.furnace.controller import Controller
from pycatalicism.furnace.owen_tpm101_controller import Owen_TPM101_Controller
from pycatalicism.furnace.furnace_exception import FurnaceException

def get_controller(controller_type:str, port:str, baudrate:int, bytesize:int, parity:str, stopbits:float, timeout:float, write_timeout:float|None, rtscts:bool, **kwargs) -> Controller:
    """
    Get furnace controller object of corresponding type

    parameters
    ----------
    controller_type:str
        type of furnace controller
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
    kwargs:dict
        Other argument relevant for concrete implementation of controller class

    returns
    -------
    controller:Controller
        furnace controller object

    raises
    ------
    FurnaceException
        If unknown type of controller was provided to method
    """
    if controller_type == 'Owen_TPM101':
        return Owen_TPM101_Controller(port=port, baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits, timeout=timeout, write_timeout=write_timeout, rtscts=rtscts, address=kwargs['address'], rsdl=kwargs['rsdl'], address_len=kwargs['address_len'])
    else:
        raise FurnaceException(f'Unknown controller type {controller_type}')
