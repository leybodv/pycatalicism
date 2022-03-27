import logging
import logging_config
# from . import calculator
from calculator import Calculator

logger = logging.getLogger(__name__)
logging_config.configure_logger(logger)

def get_calculator(reaction:str) -> Calculator:
    """
    """
    logger.debug(f'creating calculator for reaction {reaction}')
    raise NotImplementedError()
