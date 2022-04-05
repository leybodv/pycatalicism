import functools
import inspect
import logging
import sys

import config

class Logging:

    def __init__(self, func):
        """
        """
        functools.update_wrapper(self, func)
        self.func = func
        self.logging_levels = config.logging_levels

    def __get__(self, obj, type=None):
        """
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
