import logging
import logging_config as lc
import calculator

logger = logging.getLogger(__name__)
lc.configure_logger(logger)

def get_calculator(reaction:str) -> calculator.Calculator:
    """
    """
    logger.debug(f'returning calculator for {reaction}')
    raise NotImplementedError()
