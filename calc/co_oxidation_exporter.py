from pathlib import Path
import logging

from .exporter import Exporter
from .conversion import Conversion
from .selectivity import Selectivity
from .exporterexception import ExporterException
from . import logging_config

class COOxidationExporter(Exporter):
    """
    """

    def __init__(self):
        """
        """
        self.logger = logging.getLogger(__class__.__name__)
        logging_config.configure_logger(self.logger)

    def export(self, output_data_path:Path, conversion:Conversion, selectivity:Selectivity|None):
        """
        """
        if output_data_path.exists() and not output_data_path.is_dir():
            raise ExporterException(f'Data path for exporting data must be a folder')
        self._export_conversion(output_data_path, conversion)

    def _export_conversion(self, output_data_path:Path, conversion:Conversion):
        """
        """
        self.logger.info(f'Exporting conversion vs. temperature data for CO oxidation reaction to "{output_data_path.joinpath("conversion.dat")}"')
        if not output_data_path.exists():
            output_data_path.mkdir(parents=True)
        with output_data_path.joinpath('conversion.dat').open(mode='w') as f:
            sorted_conversion = conversion.get_sorted()
            f.write(str(sorted_conversion))
