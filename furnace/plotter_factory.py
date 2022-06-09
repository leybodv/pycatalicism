from pycatalicism.furnace.plotter import Plotter
from pycatalicism.furnace.simple_temp_time_plotter import SimpleTempTimePlotter
from pycatalicism.furnace.plotter_exception import PlotterException

def get_plotter(plotter_type:str) -> Plotter:
    """
    """
    if plotter_type == 'simple_temp_time_plotter':
        return SimpleTempTimePlotter()
    else:
        raise PlotterException(f'Unknown plotter type: {plotter_type}')
