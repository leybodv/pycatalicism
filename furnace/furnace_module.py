from pathlib import Path

import pycatalicism.furnace.controller_factory as controller_factory
import pycatalicism.furnace.plotter_factory as plotter_factory
import pycatalicism.furnace.exporter_factory as exporter_factory

def heat(temperature:str|int, controller_type:str, plotter_type:str, exporter_type:str, wait:str|int|None=None, show_plot:bool=False, export_plot:str|Path|None=None, export_data:str|Path|None=None):
    """
    Set furnace controller temperature to target temperature, wait for specified time in min, show plot, export plot as png image and export data of temperature vs. time if corresponding parameters were provided by user

    parameters
    ----------
    temperature:str|int
        temperature to heat furnace to
    controller_type:str
        type of PID furnace controller
    plotter_type:str
        type of plotter to plot temperature vs. time data
    exporter_type:str
        type of exporter to export temperature vs. time data
    wait:str|int|None (default:None)
        time in minutes to hold furnace at specified temperature
    show_plot:bool (default:False)
        whether to show temperature vs. time plot
    export_plot:str|Path|None (default:None)
        path to file to save temperature vs. time plot
    export_data:str|Path|None (default:None)
        path to file to save temperature vs. time data
    """
    controller = controller_factory.get_controller(controller_type)
    wait = None if wait is None else int(wait)
    data = controller.heat(int(temperature), wait)
    if export_plot or show_plot:
        plotter = plotter_factory.get_plotter(plotter_type)
        if show_plot:
            plotter.plot(data)
        if export_plot:
            plotter.export_plot(Path(export_plot).resolve())
    if export_data:
        exporter = exporter_factory.get_exporter(exporter_type)
        exporter.export_data(Path(export_data).resolve())
