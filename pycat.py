#!/usr/bin/python

"""
Module is a start point for the program. It parses arguments provided by user as command line arguments and executes corresponding functions.
"""

import argparse

import pycatalicism.calc.calc as calc
import config
from pycatalicism.calc.calculatorexception import CalculatorException

def calculate(args:argparse.Namespace):
    """
    Calculate conversion and/or selectivity (depending on --conversion/--selectivity flag provided by user) vs. temperature for CO oxidation or CO2 hydrogenation reactions, print results to console and export them if path to export directory was provided by user. Plot corresponding graphs if --show-plot argument was provided by user and export them if export directory was provided.
    """
    parser_type = config.raw_data_parser_type
    try:
        calc.calculate(input_data_path=args.input_data_path, initial_data_path=args.initial_data_path, reaction=args.reaction, parser_type=parser_type, calculate_conversion=args.conversion, calculate_selectivity=args.selectivity, products_basis=args.products_basis, output_data_path=args.output_data, show_plot=args.show_plot, output_plot_path=args.output_plot, plot_title=args.plot_title)
    except CalculatorException:
        print('At least one of the flags {--conversion|--selectivity} must be provided to the program')

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(required=True)
calc_parser = subparsers.add_parser('calc', help='calculate conversion and selectivity vs. temperature')
calc_parser.set_defaults(func=calculate)
calc_parser.add_argument('input_data_path', metavar='input-data-path', help='path to folder with files from concentration measurement device')
calc_parser.add_argument('initial_data_path', metavar='initial-data-path', help='path to file with data about initial composition of gas')
calc_parser.add_argument('reaction', choices=['co-oxidation', 'co2-hydrogenation'], help='reaction for which to calculate data')
calc_parser.add_argument('--conversion', action='store_true', help='calculate conversion for the specified reaction')
calc_parser.add_argument('--selectivity', action='store_true', help='calculate selectivities for the specified reaction')
calc_parser.add_argument('--output-data', default=None, help='path to directory to save calculated data')
calc_parser.add_argument('--show-plot', action='store_true', help='whether to show data plot or not')
calc_parser.add_argument('--output-plot', default=None, help='path to directory to save plot')
calc_parser.add_argument('--products-basis', action='store_true', help='calculate conversion based on products concentration instead of reactants')
calc_parser.add_argument('--plot-title', help='title of plot will be shown at the top')

if (__name__ == '__main__'):
    args = parser.parse_args()
    args.func(args)
