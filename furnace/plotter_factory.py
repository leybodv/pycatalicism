"""
Module creates plotter of requested type to make plots of temperature vs. time data.
"""

from pycatalicism.furnace.plotter import Plotter
from pycatalicism.furnace.simple_temp_time_plotter import SimpleTempTimePlotter
from pycatalicism.furnace.plotter_exception import PlotterException

def get_plotter(plotter_type:str) -> Plotter:
    """
    Creates plotter of requested type.

    parameters
    ----------
    plotter_type:str
        Type of plotter to use for creation of temperature vs. time graphs. Supported types:
            "simple_temp_time_plotter"
                Plots data as simple temperature vs. time graph

    returns
    -------
    plotter:Plotter
        Plotter for temperature vs. time plots creation

    raises
    ------
    PlotterException
        If Unknown plotter type was encountered.
    """
    if plotter_type == 'simple_temp_time_plotter':
        return SimpleTempTimePlotter()
    else:
        raise PlotterException(f'Unknown plotter type: {plotter_type}')
