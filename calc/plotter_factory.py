from .plotter import Plotter
from .co_oxidation_plotter import COOxidationPlotter
from .co2_hydrogenation_plotter import CO2HydrogenationPlotter
from .plotterexception import PlotterException

def get_plotter(reaction:str) -> Plotter:
    """
    """
    if reaction == 'co-oxidation':
        return COOxidationPlotter()
    elif reaction == 'co2-hydrogenation':
        return CO2HydrogenationPlotter()
    else:
        raise PlotterException(f'Cannot create plotter for reaction "{reaction}"')
