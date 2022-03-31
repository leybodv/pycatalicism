import logging

from . import logging_config
from .exporter import Exporter

logger = logging.getLogger(__name__)
logging_config.configure_logger(logger)

def get_exporter(reaction:str) -> Exporter:
    """
    """
    raise NotImplementedError()
