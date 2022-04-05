from pycatalicism.calc.exporter import Exporter
from pycatalicism.calc.co2_hydrogenation_exporter import CO2HydrogenationExporter
from pycatalicism.calc.co_oxidation_exporter import COOxidationExporter
from pycatalicism.calc.exporterexception import ExporterException

def get_exporter(reaction:str) -> Exporter:
    """
    """
    if reaction == 'co-oxidation':
        return COOxidationExporter()
    elif reaction == 'co2-hydrogenation':
        return CO2HydrogenationExporter()
    else:
        raise ExporterException(f'Cannot create exporter for reaction "{reaction}"')
