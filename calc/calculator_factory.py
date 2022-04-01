from .calculator import Calculator
from .cooxidationcalculator import COOxidationCalculator
from .co2hydrogenationcalculator import CO2HydrogenationCalculator

def get_calculator(reaction:str) -> Calculator:
    """
    """
    if reaction == 'co-oxidation':
        return COOxidationCalculator()
    elif reaction == 'co2-hydrogenation':
        return CO2HydrogenationCalculator()
    else:
        raise Exception(f'Cannot create calculator for reaction {reaction}')
