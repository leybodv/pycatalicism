#!/usr/bin/python

import logging

import logging_config
from decorator import Decorator
from test import Test

logger = logging.getLogger(__name__)
logging_config.configure_logger(logger)

@Decorator
def decorated_func():
    logger.info('started decorated_func')
    return 'return __main__.decorated_func'

if __name__ == '__main__':
    logger.info('started execution')
    decorated_func()
    t = Test()
    logger.info(f'{__main___logger = }')
    logger.info(f'{t.Test_logger = }')
