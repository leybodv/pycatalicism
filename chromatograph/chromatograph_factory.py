from pycatalicism.chromatograph.chromatograph import Chromatograph
from pycatalicism.chromatograph.chromatec_crystal_5000 import ChromatecCrystal5000
from pycatalicism.chromatograph.chromatograph_exceptions import ChromatographException

"""
"""

def get_chromatograph(chromatograph_type:str, **kwargs) -> Chromatograph:
    """
    """
    if chromatograph_type == 'chromatec_crystal_5000':
        return ChromatecCrystal5000(control_panel_id=kwargs['control_panel_id'], analytics_id=kwargs['analytics_id'], serial_id=kwargs['serial_id'], lab_name=kwargs['lab_name'], methods=kwargs['methods'], chromatograph_command_address=kwargs['chromatograph_command_address'], application_command_address=kwargs['application_command_address'], chromatograph_serial_id_address=kwargs['chromatograph_serial_id_address'], set_method_address=kwargs['set_method_address'], current_step_address=kwargs['current_step_address'], connection_status_address=kwargs['connection_status_address'], chromatogram_lab_name_address=kwargs['chromatogram_lab_name_address'], chromatogram_name_address=kwargs['chromatogram_name_address'], chromatogram_sample_volume_address=kwargs['chromatogram_sample_volume_address'], chromatogram_sample_dilution_address=kwargs['chromatogram_sample_dilution_address'], chromatogram_operator_address=kwargs['chromatogram_operator_address'], chromatogram_column_address=kwargs['chromatogram_column_address'])
    else:
        raise ChromatographException(f'Unknown type of chromatograph {chromatograph_type}')
