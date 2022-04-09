import functools
import inspect
import logging
import sys
from typing import Callable

import config

class Logging:
    """
    Class used to register and configure logger with objects or modules. In order to use it one should decorate any method in module or __init__ method in object class with Logging class. The registered logger is available as "logger" or "self.logger" instance variables
    """

    def __init__(self, func:Callable):
        """
        Assign parameter to instance variable, get logging levels from config file placed in the same directory as this module.

        parameters
        ----------
        func:Callable
            function to be decorated with this class
        """
        functools.update_wrapper(self, func)
        self.func = func
        self.logging_levels = config.logging_levels

    def __get__(self, obj:object, type=None):
        """
        When this class is initialized at import time, it does not know whether func is function or method. This method is used to overcome the problem (see https://stackoverflow.com/questions/2366713/can-a-decorator-of-an-instance-method-access-the-class/48491028#48491028)
        """
        func = self.func.__get__(obj, type)
        return self.__class__(func)

    def __call__(self, *args, **kwargs):
        """
        """
        if inspect.isfunction(self.func):
            module = sys.modules[self.func.__module__]
            if 'logger' not in module.__dict__:
                logger = logging.getLogger(module.__name__)
                self._configure_logger(logger, self.logging_levels[module.__name__])
                module.__dict__['logger'] = logger
        elif inspect.ismethod(self.func):
            obj = self.func.__self__
            if 'logger' not in obj.__dict__:
                logger = logging.getLogger(obj.__class__.__name__)
                self._configure_logger(logger, self.logging_levels[obj.__class__.__name__])
                obj.__dict__['logger'] = logger
        else:
            raise Exception(f'Cannot decorate function {self.func.__name__}')
        return self.func(*args, **kwargs)

    def _configure_logger(self, logger:logging.Logger, level:int):
        """
        """
        logger.setLevel(level)
        logger.propagate = False

        ch = logging.StreamHandler()
        ch.setLevel(level)

        formatter = logging.Formatter(fmt='[%(asctime)s] %(name)s.%(funcName)s: %(levelname)s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S')

        ch.setFormatter(formatter)

        logger.addHandler(ch)
