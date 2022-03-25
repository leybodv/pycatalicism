#!/usr/bin/python

import logging
import logging_config.logging_config as lc
import argparse
import calc
import calc.main

logger = logging.getLogger(__name__)
lc.configure_logger(logger)

def calculate(args:argparse.Namespace):
    """
    """
    logger.info('Calculating conversion and selectivity vs. temperature')
    calculator = calc.main.get_calculator(args.reaction)
    calculator.calculate(args.output_data, args.show_plot, args.output_plot)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(required=True)
calc_parser = subparsers.add_parser('calc', help='calculate conversion and selectivity vs. temperature')
calc_parser.set_defaults(func=calculate)
calc_parser.add_argument('reaction', choices=['co-oxidation', 'co2-hydrogenation'], help='reaction for which to calculate data')
calc_parser.add_argument('--output-data', default=None, help='path to file to save calculated data')
calc_parser.add_argument('--show-plot', action='store_true', help='whether to show data plot or not')
calc_parser.add_argument('--output-plot', default=None, help='path to file to save plot')

args = parser.parse_args()
args.func(args)
