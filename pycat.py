#!/usr/bin/python

import argparse

from calc import calc
import config

def calculate(args:argparse.Namespace):
    """
    """
    parser_type = config.raw_data_parser_type
    calc.calculate(input_data_path=args.input_data_path, initial_data_path=args.initial_data_path, reaction=args.reaction, parser_type=parser_type, output_data_path=args.output_data, show_plot=args.show_plot, output_plot_path=args.output_plot)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(required=True)
calc_parser = subparsers.add_parser('calc', help='calculate conversion and selectivity vs. temperature')
calc_parser.set_defaults(func=calculate)
calc_parser.add_argument('input_data_path', metavar='input-data-path', help='path to folder with files from concentration measurement device')
calc_parser.add_argument('initial_data_path', metavar='initial-data-path', help='path to file with data about initial composition of gas')
calc_parser.add_argument('reaction', choices=['co-oxidation', 'co2-hydrogenation'], help='reaction for which to calculate data')
calc_parser.add_argument('--output-data', default=None, help='path to directory to save calculated data')
calc_parser.add_argument('--show-plot', action='store_true', help='whether to show data plot or not')
calc_parser.add_argument('--output-plot', default=None, help='path to directory to save plot')

if (__name__ == '__main__'):
    args = parser.parse_args()
    args.func(args)
