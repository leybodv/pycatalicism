from pycatalicism.calc.plotter import Plotter
from pycatalicism.calc.co_oxidation_plotter import COOxidationPlotter
from pycatalicism.calc.co2_hydrogenation_plotter import CO2HydrogenationPlotter
from pycatalicism.calc.plotterexception import PlotterException

def get_plotter(reaction:str) -> Plotter:
    """
    """
    if reaction == 'co-oxidation':
        return COOxidationPlotter()
    elif reaction == 'co2-hydrogenation':
        return CO2HydrogenationPlotter()
    else:
        raise PlotterException(f'Cannot create plotter for reaction "{reaction}"')
