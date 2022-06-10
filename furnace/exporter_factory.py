from pycatalicism.furnace.exporter import Exporter
from pycatalicism.furnace.simple_temp_time_exporter import SimpleTempTimeExporter
from pycatalicism.furnace.exporter_exception import ExporterException

def get_exporter(exporter_type:str) -> Exporter:
    """
    """
    if exporter_type == 'simple_temp_time_exporter':
        return SimpleTempTimeExporter()
    else:
        raise ExporterException(f'Unknown exporter type: {exporter_type}')
