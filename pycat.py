#!/usr/bin/python

"""
Module is a start point for the program. It parses arguments provided by user as command line arguments and executes corresponding functions.
"""

import argparse

import pycatalicism.calc.calc as calc
import pycatalicism.furnace.furnace_module as furnace_module
import config
from pycatalicism.calc.calculatorexception import CalculatorException

def calculate(args:argparse.Namespace):
    """
    Calculate conversion and/or selectivity (depending on --conversion/--selectivity flag provided by user) vs. temperature for CO oxidation or CO2 hydrogenation reactions, print results to console and export them if path to export directory was provided by user. Plot corresponding graphs if --show-plot argument was provided by user and export them if export directory was provided.
    """
    parser_type = config.raw_data_parser_type
    try:
        calc.calculate(input_data_path=args.input_data_path, initial_data_path=args.initial_data_path, reaction=args.reaction, parser_type=parser_type, calculate_conversion=args.conversion, calculate_selectivity=args.selectivity, products_basis=args.products_basis, output_data_path=args.output_data, show_plot=args.show_plot, output_plot_path=args.output_plot, sample_name=args.sample_name)
    except CalculatorException:
        print('At least one of the flags {--conversion|--selectivity} must be provided to the program')

def heat(args:argparse.Namespace):
    """
    Set furnace controller temperature to specified value. If wait parameter is provided, hold furnace at specified temperature during wait time in minutes and turn heating off afterwards. Plot temperature vs. time plot if --show-plot is provided (NB: this will block execution of program until plot window is closed). Export temperature vs. time data/plot if --export-data/--export-plot arguments were provided by user.
    """
    furnace_module.heat(temperature=args.temperature, wait=args.wait, show_plot=args.show_plot, export_plot=args.export_plot, export_data=args.export_data)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(required=True)

calc_parser = subparsers.add_parser('calc', help='calculate conversion and selectivity vs. temperature')
calc_parser.set_defaults(func=calculate)
calc_parser.add_argument('input_data_path', metavar='input-data-path', help='path to directory with files from concentration measurement device')
calc_parser.add_argument('initial_data_path', metavar='initial-data-path', help='path to file with data about initial composition of gas')
calc_parser.add_argument('reaction', choices=['co-oxidation', 'co2-hydrogenation'], help='reaction for which to calculate data')
calc_parser.add_argument('--conversion', action='store_true', help='calculate conversion for the specified reaction')
calc_parser.add_argument('--selectivity', action='store_true', help='calculate selectivities for the specified reaction')
calc_parser.add_argument('--output-data', default=None, help='path to directory to save calculated data')
calc_parser.add_argument('--show-plot', action='store_true', help='whether to show data plot or not')
calc_parser.add_argument('--output-plot', default=None, help='path to directory to save plot')
calc_parser.add_argument('--products-basis', action='store_true', help='calculate conversion based on products concentration instead of reactants')
calc_parser.add_argument('--sample-name', help='sample name will be added to results data files and as a title to the result plots')

furnace_parser = subparsers.add_parser('heat', help='control furnace')
furnace_parser.set_defaults(func=heat)
furnace_parser.add_argument('temperature', help='heat furnace to target temperature')
furnace_parser.add_argument('--wait', default=None, help='time in minutes to hold furnace at the specified temperature before turning heating off')
furnace_parser.add_argument('--show-plot', action='store_true', help='show temperature vs. time plot')
furnace_parser.add_argument('--export-plot', default=None, help='path to file to save plot of temperature vs. time as png image')
furnace_parser.add_argument('--export-data', default=None, help='path to file to save temperature vs. time data')

chromatograph_parser = subparsers.add_parser('start-analysis')
chromatograph_parser.set_defaults(func=start_analysis)
chromatograph_parser.add_argument('--instrument-method', required=True, help='instrumental method to set before starting the analysis')
chromatograph_parser.add_argument('--name', required=True, help='name of chromatogram will be saved in passport')
chromatograph_parser.add_argument('--sample-volume', required=True, help='sample volume will be saved in passport')
chromatograph_parser.add_argument('--sample-dilution', required=True, help='sample dilution will be saved in passport')
chromatograph_parser.add_argument('--operator', required=True, help='operator name will be saved in passport')
chromatograph_parser.add_argument('--column', required=True, help='column name will be saved in passport')

if (__name__ == '__main__'):
    args = parser.parse_args()
    args.func(args)
