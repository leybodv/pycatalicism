class OwenTPM101():
    """
    """

    def __init__(self):
        """
        """
        self._logger = furnace_logging.get_logger(self.__class__.__name__)

    def connect(self):
        """
        """
        raise NotImplementedError()

    def set_temperature(self, temperature:float):
        """
        """
        raise NotImplementedError()

    def get_temperature(self) -> float:
        """
        """
        raise NotImplementedError()
