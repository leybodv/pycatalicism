from pycatalicism.furnace.controller import Controller
from pycatalicism.furnace.owen_tpm101_controller import Owen_TPM101_Controller
from pycatalicism.furnace.furnace_exception import FurnaceException

def get_controller(controller_type:str) -> Controller:
    """
    Get furnace controller object of corresponding type

    parameters
    ----------
    controller_type:str
        type of furnace controller

    returns
    -------
    controller:Controller
        furnace controller object
    """
    if controller_type == 'Owen_TPM101':
        return Owen_TPM101_Controller()
    else:
        raise FurnaceException(f'Unknown controller type {controller_type}')
