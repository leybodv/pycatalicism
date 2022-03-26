import logging
import logger_config
from pathlib import Path

logger = logging.getLogger(__name__)

def _export_results(output_data_path:Path, conversion, selectivity):
    """
    """
    raise NotImplementedError()

def calculate(reaction:str, output_data_path:Path|None=None, show_plot:bool=False, output_plot_path:Path|None=None):
    """
    """
    logger.info(f'calculating conversion and selectivity for reaction {reaction}')
    conversion = calculator.calculate_conversion(input_data)
    selectivity = calculator.calculate_selectivity(input_data)
    _print_results(conversion, selectivity)
    if ouput_data_path is not None:
        _export_results(output_data_path, conversion, selectivity)
    if show_plot or (output_plot_path is not None):
        plotter.plot(conversion, selectivity, show_plot, output_plot_path)
