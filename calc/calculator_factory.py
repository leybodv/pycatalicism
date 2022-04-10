from pycatalicism.calc.calculator import Calculator
from pycatalicism.calc.cooxidationcalculator import COOxidationCalculator
from pycatalicism.calc.co2hydrogenationcalculator import CO2HydrogenationCalculator

"""
Factory to create calculator for proper reaction.
"""

def get_calculator(reaction:str) -> Calculator:
    """
    Create calculator for reaction to calculate conversion, selectivity or activity vs. temperature data.

    parameters
    ----------
    reaction:str {co-oxidation|co2-hydrogenation}
        Chemical reaction for which to calculate results

    returns
    -------
    calculator:Calculator
        Calculator to use for catalyst characteristics calculation

    raises
    ------
    exception:Exception
        if reaction is not known
    """
    if reaction == 'co-oxidation':
        return COOxidationCalculator()
    elif reaction == 'co2-hydrogenation':
        return CO2HydrogenationCalculator()
    else:
        raise Exception(f'Cannot create calculator for reaction {reaction}')
