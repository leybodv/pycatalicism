import logging
from logging import Logger

"""
module responsible for logger configuration
"""

level = logging.INFO

def configure_logger(logger: Logger):
    """
    set loggers level, handler and formatter

    parameters
    ----------
        logger:Logger
            logger to be configured
    """
    logger.setLevel(level)
    logger.propagate = False

    ch = logging.StreamHandler()
    ch.setLevel(level)

    formatter = logging.Formatter(fmt='[%(asctime)s] %(name)s.%(funcName)s: %(levelname)s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S')

    ch.setFormatter(formatter)

    logger.addHandler(ch)
