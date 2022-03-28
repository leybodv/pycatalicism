import logging

from . import logging_config
from .calculator import Calculator

class COOxidationCalculator(Calculator):
    """
    """

    def __init__(self):
        """
        """
        self.logger = logging.getLogger(__class__.__name__)
        logging_config.configure_logger(self.logger)
        self.logger.debug(f'creating {__class__.__name__}')
