from pycatalicism.calc.exporter import Exporter
from pycatalicism.calc.co2_hydrogenation_exporter import CO2HydrogenationExporter
from pycatalicism.calc.co_oxidation_exporter import COOxidationExporter
from pycatalicism.calc.exporterexception import ExporterException

"""
Factory for creating exporters for specified reaction.
"""

def get_exporter(reaction:str) -> Exporter:
    """
    Get exporter for specified reaction.

    parameters
    ----------
    reaction:str {co-oxidation|co2-hydrogenration}
        chemical reaction to export calculated results

    returns
    -------
    exporter:Exporter
        concrete exporter object for specified reaction

    raises
    ------
    exception:ExporterException
        if reaction is not known
    """
    if reaction == 'co-oxidation':
        return COOxidationExporter()
    elif reaction == 'co2-hydrogenation':
        return CO2HydrogenationExporter()
    else:
        raise ExporterException(f'Cannot create exporter for reaction "{reaction}"')
