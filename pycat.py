#!/usr/bin/python

import logging
import logging_config
import argparse

logger = logging.getLogger(__name__)
logging_config.configure_logger(logger)

def calculate(args:argparse.Namespace):
    """
    """
    logger.info('Calculating conversion and selectivity vs. temperature')
    raise NotImplementedError()

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(required=True)
calc = subparsers.add_parser('calc', help='calculate conversion and selectivity vs. temperature')
calc.set_defaults(func=calculate)
calc.add_argument('reaction', choices=['co-oxidation', 'co2-hydrogenation'], help='reaction for which to calculate data')
calc.add_argument('--output-data', help='path to file to save calculated data')
calc.add_argument('--show-plot', action='store_true', help='whether to show data plot or not')
calc.add_argument('--output-plot', help='path to file to save plot')

args = parser.parse_args()
args.func(args)
