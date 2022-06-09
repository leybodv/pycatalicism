from pycatalicism.furnace.plotter import Plotter

def get_plotter(plotter_type:str) -> Plotter:
    """
    """
    if plotter_type == 'simple_temp_time_plotter':
        return SimpleTempTimePlotter()
    else:
        raise PlotterException(f'Unknown plotter type: {plotter_type}')
