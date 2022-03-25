import logging
from logging import Logger

level = logging.DEBUG

def configure_logger(logger: Logger):
    """
    """
    logger.setLevel(level)
    logger.propagate = False

    ch = logging.StreamHandler()
    ch.setLevel(level)

    formatter = logging.Formatter(fmt='[%(asctime)s] %(name)s.%(funcName)s: %(levelname)s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S')

    ch.setFormatter(formatter)

    logger.addHandler(ch)
