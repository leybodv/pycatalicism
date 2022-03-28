#!/usr/bin/python

import logging
import argparse

import logging_config as lc
from calc import calc

logger = logging.getLogger(__name__)
lc.configure_logger(logger)

def calculate(args:argparse.Namespace):
    """
    """
    logger.info(f'Calculating conversion and selectivity vs. temperature for reaction {args.reaction}')
    calc.calculate(input_data_path=args.input_data_path, reaction=args.reaction, parser_type=parser_type, output_data_path=args.output_data, show_plot=args.show_plot, output_plot_path=args.output_plot)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(required=True)
calc_parser = subparsers.add_parser('calc', help='calculate conversion and selectivity vs. temperature')
calc_parser.set_defaults(func=calculate)
calc_parser.add_argument('input_data_path', metavar='input-data-path', help='path to folder with files from concentration measurement device')
calc_parser.add_argument('reaction', choices=['co-oxidation', 'co2-hydrogenation'], help='reaction for which to calculate data')
calc_parser.add_argument('--output-data', default=None, help='path to file to save calculated data')
calc_parser.add_argument('--show-plot', action='store_true', help='whether to show data plot or not')
calc_parser.add_argument('--output-plot', default=None, help='path to file to save plot')

if (__name__ == '__main__'):
    args = parser.parse_args()
    args.func(args)
