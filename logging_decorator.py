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
            self._configure_logger(logger)
        elif inspect.ismethod(self.func):
            obj = self.func.__self__
            obj.logger = logging.getLogger(obj.__class__.__name__)
            self._configure_logger(obj.logger)
        else:
            raise Exception(f'Cannot decorate function {self.func.__name__}')
        return self.func(*args, **kwargs)

    def _configure_logger(self, logger:logging.Logger):
        """
        """
        raise NotImplementedError()
