from pycatalicism.chromatograph.chromatograph import Chromatograph
from pycatalicism.chromatograph.chromatec_crystal_5000 import ChromatecCrystal5000
from pycatalicism.chromatograph.chromatograph_exception import ChromatographException

"""
"""

def get_chromatograph(chromatograph_type:str) -> Chromatograph:
    """
    """
    if chromatograph_type == 'chromatec_crystal_5000':
        return ChromatecCrystal5000()
    else:
        raise ChromatographException(f'Unknown type of chromatograph {chromatograph_type}')
