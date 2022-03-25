import logging
import logging_config as lc
import calc.calculator as calculator

logger = logging.getLogger(__name__)
lc.configure_logger(logger)

def get_calculator(reaction:str) -> calculator.Calculator:
    """
    """
    logger.debug(f'returning calculator for {reaction}')
    if reaction == 'co-oxidation':
        from cooxidationcalculator import COOxidationCalculator
        return COOxidationCalculator()
    elif reaction == 'co2-hydrogenation':
        from co2hydrogenationcalculator import CO2HydrogenationCalculator
        return CO2HydrogenationCalculator()
    else:
        raise Exception(f'Unknown reaction "{reaction}"')
