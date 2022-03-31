import logging
from pathlib import Path

from . import logging_config
from . import calculator_factory
from . import parser_factory
from . import exporter_factory
from . import plotter_factory

logger = logging.getLogger(__name__)
logging_config.configure_logger(logger)

def _print_results(conversion, selectivity):
    """
    """
    print(conversion)
    print(selectivity)

def calculate(input_data_path:str, initial_data_path:str, reaction:str, parser_type:str, output_data_path:str|None=None, show_plot:bool=False, output_plot_path:str|None=None):
    """
    """
    calculator = calculator_factory.get_calculator(reaction)
    parser = parser_factory.get_parser(parser_type)
    input_data = parser.parse_data(Path(input_data_path).resolve(), Path(initial_data_path).resolve())
    conversion = calculator.calculate_conversion(input_data)
    selectivity = calculator.calculate_selectivity(input_data)
    _print_results(conversion, selectivity)
    if output_data_path is not None:
        exporter = exporter_factory.get_exporter(reaction)
        exporter.export(Path(output_data_path).resolve(), conversion, selectivity)
    if show_plot or (output_plot_path is not None):
        plotter = plotter_factory.get_plotter(reaction)
        path = None if output_plot_path is None else Path(output_plot_path).resolve()
        plotter.plot(conversion, selectivity, show_plot, path)
