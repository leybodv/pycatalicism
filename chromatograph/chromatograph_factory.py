from pycatalicism.chromatograph.crystal_5000_chromatec import Crystal5000Chromatec
from pycatalicism.chromatograph.exceptions.connection_error import ConnectionError

"""
"""

def get_crystal_5000_chromatec(self, control_panel_id:int, analytics_id:int) -> Crystal5000Chromatec:
    """
    """
    chromatograph = Crystal5000Chromatec(control_panel_id, analytics_id)
    if not chromatograph.connect():
        raise ConnectionError('Could not connect to Chromatec Crystal 5000 chromatograph')
    return chromatograph
