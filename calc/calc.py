from pathlib import Path

from pycatalicism.calc import calculator_factory
from pycatalicism.calc import parser_factory
from pycatalicism.calc import exporter_factory
from pycatalicism.calc import plotter_factory
from pycatalicism.calc.conversion import Conversion
from pycatalicism.calc.selectivity import Selectivity
from pycatalicism.calc.calculatorexception import CalculatorException

"""
Main interface for calculating conversion, activity and selectivity of catalysts. Users of this module should use calculate method to perform all calculation tasks.
"""


def _print_results(conversion:Conversion, selectivity:Selectivity):
    """
    Print results for conversion and selectivities vs. temperature to console.

    parameters
    ----------
    conversion:Conversion
        Reactant conversions at different temperatures data wrapper
    selectivity:Selectivity
        Catalyst selectivities for different product components at different temperatures data wrapper
    """
    if conversion:
        print(conversion)
    if selectivity:
        print(selectivity)

def calculate(input_data_path:str, initial_data_path:str, reaction:str, parser_type:str, calculate_conversion:bool, calculate_selectivity:bool, output_data_path:str|None=None, show_plot:bool=False, output_plot_path:str|None=None):
    """
    Main interface to module. Parses input data from equipment capable of measuring composition and, ideally, initial and final gas total flow rate. Calculates conversion and selectivity data from input data. Prints results to console. If output_data_path was provided exports results. If show_plot is True, shows resulting plots. If output_plot_path was provided, exports corresponding plots.

    parameters
    ----------
    input_data_path:str
        Path to directory with input data files
    initial_data_path:str
        Path to file with gas composition data without catalyst (i.e. no reaction occured)
    reaction:str {co-oxidation|co2-hydrogenation}
        Chemical reaction to calculate data for
    parser_type:str {chromatec-crystal-composition-copy-paste}
        Parser type to use for parsing input data
    output_data_path:str|None {default:None}
        Path to directory to export results in text format
    show_plot:bool {default:False}
        Whether to show resulting plot
    output_plot_path:str|None {default:None}
        Path to directory to export resulting plot
    """
    if not (calculate_conversion and calculate_selectivity):
        raise CalculatorException('Nothing to calculate')
    calculator = calculator_factory.get_calculator(reaction)
    parser = parser_factory.get_parser(parser_type)
    input_data = parser.parse_data(Path(input_data_path).resolve(), Path(initial_data_path).resolve())
    conversion = None
    selectivity = None
    if calculate_conversion:
        conversion = calculator.calculate_conversion(input_data)
    if calculate_selectivity:
        selectivity = calculator.calculate_selectivity(input_data)
    _print_results(conversion, selectivity)
    if output_data_path is not None:
        exporter = exporter_factory.get_exporter(reaction)
        exporter.export(Path(output_data_path).resolve(), conversion, selectivity)
    if show_plot or (output_plot_path is not None):
        plotter = plotter_factory.get_plotter(reaction)
        path = None if output_plot_path is None else Path(output_plot_path).resolve()
        plotter.plot(conversion, selectivity, show_plot, path)
