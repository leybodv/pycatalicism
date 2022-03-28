import logging

from . import logging_config
from .calculator import Calculator

class CO2HydrogenationCalculator(Calculator):
    """
    """

    def __init__(self):
        """
        """
        self.logger = logging.getLogger(__class__.__name__)
        logging_config.configure_logger(self.logger)
        raise NotImplementedError()
