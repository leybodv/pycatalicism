import functools
import inspect
import logging

from . import config

class Logging:

    def __init__(self, func):
        """
        """
        functools.update_wrapper(self, func)
        self.func = func
        self.logging_levels = config.logging_levels

    def __call__(self, *args, **kwargs):
        """
        """
        if inspect.isfunction(self.func):
            logger = logging.getLogger(self.func.__module__)
            self._configure_logger(logger, self.logging_levels[self.func.__module__])
        elif inspect.ismethod(self.func):
            obj = self.func.__self__
            obj.logger = logging.getLogger(obj.__class__.__name__)
            self._configure_logger(obj.logger, self.logging_levels[obj.__class__.__name__])
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
