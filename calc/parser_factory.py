from .parser import Parser
from .chromatec_crystal_composition_copy_paste_parser import ChromatecCrystalCompositionCopyPasteParser

def get_parser(parser_type:str) -> Parser:
    """
    """
    if parser_type == 'chromatec-crystal-composition-copy-paste':
        return ChromatecCrystalCompositionCopyPasteParser()
    else:
        raise Exception(f'cannot create parser for {parser_type}')
