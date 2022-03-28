import logging

from calc import logging_config
from calc.calculator import Calculator
from calc.cooxidationcalculator import COOxidationCalculator
from calc.co2hydrogenationcalculator import CO2HydrogenationCalculator

logger = logging.getLogger(__name__)
logging_config.configure_logger(logger)

def get_calculator(reaction:str) -> Calculator:
    """
    """
    logger.debug(f'creating calculator for reaction {reaction}')
    if reaction == 'co-oxidation':
        return COOxidationCalculator()
    elif reaction == 'co2-hydrogenation':
        return CO2HydrogenationCalculator()
    else:
        raise Exception(f'Cannot create calculator for reaction {reaction}')
