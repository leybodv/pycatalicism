from .plotter import Plotter
from .co_oxidation_plotter import COOxidationPlotter
from .plotterexception import PlotterException

def get_plotter(reaction:str) -> Plotter:
    """
    """
    if reaction == 'co-oxidation':
        return COOxidationPlotter()
    else:
        raise PlotterException(f'Cannot create plotter for reaction "{reaction}"')
