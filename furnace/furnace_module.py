from pathlib import Path

def heat(temperature:str|int, wait:str|int|None=None, show_plot:bool=False, export_plot:str|Path|None=None, export_data:str|Path|None=None):
    """
    """
    raise NotImplementedError()
    controller = controller_factory.get_controller(controller_type)
    data = controller.heat(temperature, wait)
    if show_plot:
        plotter = plotter_factory.get_plotter()
