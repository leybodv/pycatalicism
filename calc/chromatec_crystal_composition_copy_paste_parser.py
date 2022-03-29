import logging
from pathlib import Path

from . import logging_config
from .parser import Parser
from .rawdata import RawData

class ChromatecCrystalCompositionCopyPasteParser(Parser):
    """
    """

    def __init__(self):
        """
        """
        self.logger = logging.getLogger(__class__.__name__)
        logging_config.configure_logger(self.logger)
        self.logger.debug(f'creating {__class__.__name__}')

    def parse_data(self, input_data_path:Path) -> RawData:
        """
        """
        self.logger.debug(f'parsing data from {input_data_path}')
        raise NotImplementedError()
        return rawdata
