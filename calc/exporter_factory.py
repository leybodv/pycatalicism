from .exporter import Exporter
from .co_oxidation_exporter import COOxidationExporter
from .exporterexception import ExporterException

def get_exporter(reaction:str) -> Exporter:
    """
    """
    if reaction == 'co-oxidation':
        return COOxidationExporter()
    else:
        raise ExporterException(f'Cannot create exporter for reaction "{reaction}"')
