import logging
from logging import Logger

def configure_logger(logger: Logger, level:int):
    """
    """
    logger.setLevel(level)
    logger.propagate = False

    ch = logging.StreamHandler()
    ch.setLevel(level)

    formatter = logging.Formatter(fmt='[%(asctime)s] %(name)s.%(funcName)s: %(levelname)s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S')

    ch.setFormatter(formatter)

    logger.addHandler(ch)
