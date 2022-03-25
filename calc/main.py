import logging
import logging_config

logger = logging.getLogger(__name__)
logging_config.configure_logger(logger)

def get_calculator(reaction:str) -> calculator.Calculator:
    """
    """
    logger.debug(f'returning calculator for {reaction}')
    raise NotImplementedError()
