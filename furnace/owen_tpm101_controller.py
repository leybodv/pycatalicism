from pycatalicism.furnace.controller import Controller
from pycatalicism.furnace.furnace_data import FurnaceData

class Owen_TPM101_Controller(Controller):
    """
    """

    def heat(self, temperature:int, wait:int|None) -> FurnaceData:
        """
        """
        raise NotImplementedError()
