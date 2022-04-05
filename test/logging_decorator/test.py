from decorator import Decorator
import inspect
import logging

import logging_config

print('\t\tAccess to test.py')

class Test:

    @Decorator
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        logging_config.configure_logger(self.logger)
