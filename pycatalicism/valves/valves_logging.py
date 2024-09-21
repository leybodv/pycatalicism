"""
Module for instantiating and configuring logger
"""

import logging
from pathlib import Path

from pycatalicism.valves.logging_config import logging_levels

def get_logger(name:str, logfilename:str) -> logging.Logger:
    """
    Get logger with corresponding name configured to log to stdout.

    parameters
    ----------
    name:str
        name of returned logger
    logfilename:str
        name of file to write logs to

    returns
    -------
    logger:logging.Logger
        configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging_levels[name])
    logger.propagate = False

    logfile = Path(logfilename).absolute()
    logfile.parent.mkdir(parents=True, exist_ok=True)
    if not logger.handlers:
        ch = logging.StreamHandler()
        fh = logging.FileHandler(filename=logfile)
        ch.setLevel(logging_levels[name])
        fh.setLevel(logging_levels[name])
        formatter = logging.Formatter(fmt='[%(asctime)s] %(name)s.%(funcName)s: %(levelname)s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        logger.addHandler(ch)
        logger.addHandler(fh)
    return logger
