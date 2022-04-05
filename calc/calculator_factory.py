from pycatalicism.calc.calculator import Calculator
from pycatalicism.calc.cooxidationcalculator import COOxidationCalculator
from pycatalicism.calc.co2hydrogenationcalculator import CO2HydrogenationCalculator

def get_calculator(reaction:str) -> Calculator:
    """
    """
    if reaction == 'co-oxidation':
        return COOxidationCalculator()
    elif reaction == 'co2-hydrogenation':
        return CO2HydrogenationCalculator()
    else:
        raise Exception(f'Cannot create calculator for reaction {reaction}')
