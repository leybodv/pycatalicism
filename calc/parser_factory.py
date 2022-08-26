from calc.parser import Parser
from calc.parserexception import ParserException
from calc.chromatec_crystal_composition_copy_paste_parser import ChromatecCrystalCompositionCopyPasteParser

"""
Factory for creating parser for specific data format.
"""

def get_parser(parser_type:str) -> Parser:
    """
    Get parser for specified data format.

    parameters
    ----------
    parser_type:str {chromatec-crystal-composition-copy-paste}
        parser type representing certain data format

    raises
    ------
    exception:ParserException
        if parser type is not known
    """
    if parser_type == 'chromatec-crystal-composition-copy-paste':
        return ChromatecCrystalCompositionCopyPasteParser()
    else:
        raise ParserException(f'cannot create parser for {parser_type}')
