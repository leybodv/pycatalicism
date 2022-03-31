from pathlib import Path

from .exporter import Exporter
from .conversion import Conversion
from .selectivity import Selectivity
from .exporterexception import ExporterException

class COOxidationExporter(Exporter):
    """
    """

    def export(self, output_data_path:Path, conversion:Conversion, selectivity:Selectivity|None):
        """
        """
        if not output_data_path.is_dir():
            raise ExporterException(f'Data path for exporting data must be a folder')
        self._export_conversion(output_data_path, conversion)

    def _export_conversion(self, output_data_path:Path, conversion:Conversion):
        """
        """
        if not output_data_path.exists():
            output_data_path.mkdir(parents=True)
        with output_data_path.joinpath('conversion.dat').open(mode='w') as f:
            sorted_conversion = conversion.get_sorted()
            f.write(str(sorted_conversion))
