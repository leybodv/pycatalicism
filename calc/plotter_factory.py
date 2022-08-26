from calc.plotter import Plotter
from calc.co_oxidation_plotter import COOxidationPlotter
from calc.co2_hydrogenation_plotter import CO2HydrogenationPlotter
from calc.plotterexception import PlotterException

"""
Factory for creation of resulting data plotters.
"""

def get_plotter(reaction:str) -> Plotter:
    """
    Get plotter for specified reaction

    parameters
    ----------
    reaction:str {co-oxidation|co2-hydrogenation}
        chemical reaction of interest

    returns
    -------
    plotter:Plotter
        plotter for specified reaction

    raises
    ------
    exception:PlotterException
        if unknown reaction provided as parameter
    """
    if reaction == 'co-oxidation':
        return COOxidationPlotter()
    elif reaction == 'co2-hydrogenation':
        return CO2HydrogenationPlotter()
    else:
        raise PlotterException(f'Cannot create plotter for reaction "{reaction}"')
