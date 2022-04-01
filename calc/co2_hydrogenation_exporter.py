from pathlib import Path
import logging

from .exporter import Exporter
from .conversion import Conversion
from .selectivity import Selectivity
from .exporterexception import ExporterException
from . import logging_config

class CO2HydrogenationExporter(Exporter):
    """
    """

    def __init__(self):
        """
        """
        self.logger = logging.getLogger(__class__.__name__)
        logging_config.configure_logger(self.logger)

    def export(self, output_data_path:Path, conversion:Conversion, selectivity:Selectivity):
        """
        """
        if output_data_path.exists() and not output_data_path.is_dir():
            raise ExporterException(f'Data path for exporting data must be a folder')
        self._export_conversion(output_data_path, conversion)
        self._export_selectivity(output_data_path, selectivity)

    def _export_conversion(self, output_data_path:Path, conversion:Conversion):
        """
        """
        self.logger.info(f'Exporting conversion vs. temperature data for CO2 hydrogenation reaction to "{output_data_path.joinpath("conversion.dat")}"')
        if not output_data_path.exists():
            output_data_path.mkdir(parents=True)
        with output_data_path.joinpath('selectivity.dat').open(mode='w') as f:
            f.write(str(conversion))
