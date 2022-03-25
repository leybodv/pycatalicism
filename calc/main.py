import logging
import pycatalicism.logging_config.logging_config as lc

logger = logging.getLogger(__name__)
lc.configure_logger(logger)

def get_calculator(reaction:str) -> calculator.Calculator:
    """
    """
    logger.debug(f'returning calculator for {reaction}')
    raise NotImplementedError()
