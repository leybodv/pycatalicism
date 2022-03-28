import logging

from calc import logging_config
from calc.parser import Parser

logger = logging.getLogger(__name__)
logging_config.configure_logger(logger)

def get_parser(parser_type:str) -> Parser:
    """
    """
    raise NotImplementedError()
