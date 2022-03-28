import logging

from . import logging_config
from .parser import Parser
from .chromatec_crystal_composition_copy_paste_parser import ChromatecCrystalCompositionCopyPasteParser

logger = logging.getLogger(__name__)
logging_config.configure_logger(logger)

def get_parser(parser_type:str) -> Parser:
    """
    """
    logger.debug(f'creating parser for {parser_type}')
    if parser_type == 'chromatec-crystal-composition-copy-paste':
        return ChromatecCrystalCompositionCopyPasteParser()
    else:
        raise Exception(f'cannot create parser for {parser_type}')
