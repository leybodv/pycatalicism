from pathlib import Path

from pycatalicism.calc.exporter import Exporter
from pycatalicism.calc.conversion import Conversion
from pycatalicism.calc.selectivity import Selectivity
from pycatalicism.calc.exporterexception import ExporterException
from pycatalicism.logging_decorator import Logging

class CO2HydrogenationExporter(Exporter):
    """
    """

    @Logging
    def __init__(self):
        """
        """
        super().__init__()

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
        with output_data_path.joinpath('conversion.dat').open(mode='w') as f:
            f.write(str(conversion))

    def _export_selectivity(self, output_data_path:Path, selectivity:Selectivity):
        """
        """
        self.logger.info(f'Exporting selectivities vs. temperature data for CO2 hydrogenation reaction to "{output_data_path.joinpath("selectivity.dat")}"')
        if not output_data_path.exists():
            output_data_path.mkdir(parents=True)
        with output_data_path.joinpath('selectivity.dat').open(mode='w') as f:
            f.write(str(selectivity))

