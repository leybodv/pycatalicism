"""
Module creates concrete implementations of Exporter class using exporter type parameter
"""

from pycatalicism.furnace.exporter import Exporter
from pycatalicism.furnace.simple_temp_time_exporter import SimpleTempTimeExporter
from pycatalicism.furnace.exporter_exception import ExporterException

def get_exporter(exporter_type:str) -> Exporter:
    """
    Create exporter of corresponding type.

    parameters
    ----------
    exporter_type:str
        Type of exporter to use. Supported types:
            "simple_temp_time_exporter"
                Exports data in a format defined in __str__ method of FurnaceData class

    returns
    -------
    exporter:Exporter
        Object responsible for export of time-temperature data

    raises
    ------
    ExporterException
        If unknown exporter type was provided to method
    """
    if exporter_type == 'simple_temp_time_exporter':
        return SimpleTempTimeExporter()
    else:
        raise ExporterException(f'Unknown exporter type: {exporter_type}')
