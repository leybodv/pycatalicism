"""
Module is an entry point for package. It performs all operations relevant for furnace control.
"""

from pathlib import Path

import pycatalicism.furnace.controller_factory as controller_factory
import pycatalicism.furnace.plotter_factory as plotter_factory
import pycatalicism.furnace.exporter_factory as exporter_factory

def heat(temperature:str|int, controller_type:str, plotter_type:str, exporter_type:str, port:str, baudrate:int, bytesize:int, parity:str, stopbits:float, timeout:float, write_timeout:float, rtscts:bool, fig_dpi:float, fig_height:float, fig_width:float, wait:str|int|None=None, show_plot:bool=False, export_plot:str|Path|None=None, export_data:str|Path|None=None, **kwargs:dict):
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
    port:str
        COMM port through which connection with controller is made
    baudrate:int
        Data exchange rate, must match the one at the controller device
    bytesize:int
        Size of byte of information to be sent to the controller
    parity:str
        Whether to control parity
    stopbits:float
        How many stopbits to use when sending information to the device
    timeout:float
        Read timeout in seconds. See pyserial documentation for details (https://pyserial.readthedocs.io/en/latest/pyserial_api.html)
    write_timeout:float
        Write timeout in seconds. See pyserial documentation for details (https://pyserial.readthedocs.io/en/latest/pyserial_api.html)
    rtscts:bool
        Enable hardware flow control. See pyserial documentation for details (https://pyserial.readthedocs.io/en/latest/pyserial_api.html)
    fig_dpi:float
        resolution to use for plot export
    fig_height:float
        Height of figure in pixels to use for plot export
    fig_width:float
        Width of figure in pixels to use for plot export
    wait:str|int|None (default:None)
        time in minutes to hold furnace at specified temperature
    show_plot:bool (default:False)
        whether to show temperature vs. time plot
    export_plot:str|Path|None (default:None)
        path to file to save temperature vs. time plot
    export_data:str|Path|None (default:None)
        path to file to save temperature vs. time data
    kwargs:dict
        Other arguments relevant for concrete implementation of furnace controller class
    """
    controller = controller_factory.get_controller(controller_type=controller_type, port=port, baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits, timeout=timeout, write_timeout=write_timeout, rtscts=rtscts, kwargs=kwargs)
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
