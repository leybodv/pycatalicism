from pathlib import Path

from .exporter import Exporter
from .conversion import Conversion
from .selectivity import Selectivity

class COOxidationExporter(Exporter):
    """
    """

    def export(self, output_data_path:Path, conversion:Conversion, selectivity:Selectivity|None):
        """
        """
        raise NotImplementedError()
