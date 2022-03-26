#!/usr/bin/python

import logging
import logging_config
from pathlib import Path

logger = logging.getLogger(__name__)
logging_config.configure_logger(logger)

def _export_results(output_data_path:Path, conversion, selectivity):
    """
    """
    logger.debug(f'exporting results to {output_data_path}')
    raise NotImplementedError()

def _print_results(conversion, selectivity):
    """
    """
    logger.debug('printing results')
    raise NotImplementedError()

def calculate(input_data_path:Path, reaction:str, output_data_path:Path|None=None, show_plot:bool=False, output_plot_path:Path|None=None):
    """
    """
    import calculator_factory
    import parser_factory
    logger.info(f'calculating conversion and selectivity for reaction {reaction}')
    calculator = calculator_factory.get_calculator(reaction)
    parser = parser_factory.get_parser()
    input_data = parser.parse_data(input_data_path)
    conversion = calculator.calculate_conversion(input_data)
    selectivity = calculator.calculate_selectivity(input_data)
    _print_results(conversion, selectivity)
    if output_data_path is not None:
        _export_results(output_data_path, conversion, selectivity)
    if show_plot or (output_plot_path is not None):
        plotter.plot(conversion, selectivity, show_plot, output_plot_path)

if __name__ == '__main__':
    logger.info('executing calc.py')
