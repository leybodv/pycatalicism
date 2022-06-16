"""
Module is an entry point for package. It performs all operations relevant for furnace control.
"""

from pathlib import Path

import pycatalicism.furnace.furnace_config as config
import pycatalicism.furnace.controller_factory as controller_factory
import pycatalicism.furnace.plotter_factory as plotter_factory
import pycatalicism.furnace.exporter_factory as exporter_factory

def heat(temperature:str|int, wait:str|int|None=None, show_plot:bool=False, export_plot:str|Path|None=None, export_data:str|Path|None=None):
    """
    Set furnace controller temperature to target temperature, wait for specified time in min, show plot, export plot as png image and export data of temperature vs. time if corresponding parameters were provided by user

    parameters
    ----------
    temperature:str|int
        temperature to heat furnace to
    wait:str|int|None (default:None)
        time in minutes to hold furnace at specified temperature
    show_plot:bool (default:False)
        whether to show temperature vs. time plot
    export_plot:str|Path|None (default:None)
        path to file to save temperature vs. time plot
    export_data:str|Path|None (default:None)
        path to file to save temperature vs. time data
    """
    controller_type = config.controller_type
    port = config.port
    baudrate = config.baudrate
    bytesize = config.bytesize
    parity = config.parity
    stopbits = config.stopbits
    timeout = config.timeout
    write_timeout = config.write_timeout
    rtscts = config.rtscts
    plotter_type = config.plotter_type
    exporter_type = config.exporter_type
    fig_dpi = config.fig_dpi
    fig_height = config.fig_height
    fig_width = config.fig_width
    controller = controller_factory.get_controller(controller_type=controller_type, port=port, baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits, timeout=timeout, write_timeout=write_timeout, rtscts=rtscts, address=config.address, rsdl=config.rsdl, address_len=config.address_len)
    wait = None if wait is None else int(wait)
    data = controller.heat(int(temperature), wait)
    if export_plot or show_plot:
        plotter = plotter_factory.get_plotter(plotter_type)
        if show_plot:
            plotter.plot(data)
        if export_plot:
            plotter.export_plot(data, Path(export_plot).resolve(), fig_dpi, fig_height, fig_width)
    if export_data:
        exporter = exporter_factory.get_exporter(exporter_type)
        exporter.export_data(data, Path(export_data).resolve())
