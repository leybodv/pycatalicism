import inspect
import sys
import logging

import logging_config

log_dict = {'__main__':logging.INFO,
            'Test':logging.INFO}

class Decorator:

    def __init__(self, decor_func):
        self.logger = logging.getLogger(self.__class__.__name__)
        logging_config.configure_logger(self.logger)
        self.func = decor_func

    def __get__(self, obj, type=None):
        new_func = self.func.__get__(obj, type)
        return self.__class__(new_func)

    def __call__(self, *args, **kwargs):
        if inspect.isfunction(self.func):
            module = sys.modules[self.func.__module__]
            if f'{module.__name__}_logger' not in module.__dict__:
                module.__dict__[f'{module.__name__}_logger'] = log_dict[module.__name__]
            self.logger.info(f'{module = }')
            self.logger.info(f'{module.__dict__ = }')
        elif inspect.ismethod(self.func):
            obj = self.func.__self__
            if f'{obj.__class__.__name__}_logger' not in obj.__dict__:
                obj.__dict__[f'{obj.__class__.__name__}_logger'] = log_dict[obj.__class__.__name__]
            self.logger.info(f'{obj = }')
            self.logger.info(f'{obj.__dict__ = }')
        val = self.func(*args, **kwargs)
        return val
