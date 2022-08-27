from pathlib import Path

from calc.exporter import Exporter
from calc.conversion import Conversion
from calc.selectivity import Selectivity
from calc.exporterexception import ExporterException
from logger.logging_decorator import Logging

class CO2HydrogenationExporter(Exporter):
    """
    Class for exporting conversion and selectivity data for CO2 hydrogenation reaction to conversion.dat and selectivity.dat to a directory provided by user of this class.
    """

    @Logging
    def __init__(self):
        """
        Registers logger with instances of this class which can be accessed via self.logger instance variable.
        """
        super().__init__()

    def export(self, output_data_path:Path, conversion:Conversion, selectivity:Selectivity):
        """
        Main interface of this class. Exports conversion and selectivity data for CO2 hydrogenation reaction to conversion.dat and selectivity.dat to a directory provided by user of this method.

        parameters
        ----------
        output_data_path:Path
            path to directory to export resulting data
        conversion:Conversion
            wrapper of CO2 conversion at different temperatures
        selectivity:Selectivity
            wrapper of selectivities to different compounds at different temperatures

        raises
        ------
        exception:ExporterException
            if ouput_data_path exists and not directory
        """
        if output_data_path.exists() and not output_data_path.is_dir():
            raise ExporterException(f'Data path for exporting data must be a folder')
        self._export_conversion(output_data_path, conversion)
        self._export_selectivity(output_data_path, selectivity)

    def _export_conversion(self, output_data_path:Path, conversion:Conversion):
        """
        Export CO2 conversion data to conversion.dat at output_data_path directory

        parameters
        ----------
        ouput_data_path:Path
            path to directory to export conversion data
        conversion:Conversion
            wrapper of CO2 conversion at different temperatures
        """
        self.logger.info(f'Exporting conversion vs. temperature data for CO2 hydrogenation reaction to "{output_data_path.joinpath("conversion.dat")}"')
        if not output_data_path.exists():
            output_data_path.mkdir(parents=True)
        with output_data_path.joinpath('conversion.dat').open(mode='w') as f:
            f.write(str(conversion))

    def _export_selectivity(self, output_data_path:Path, selectivity:Selectivity):
        """
        Export selectivity data to selectivity.dat at output_data_path directory

        parameters
        ----------
        output_data_path:Path
            path to directory to export selectivity data
        selectivity:Selectivity
            wrapper of selectivities to different compounds at different temperatures
        """
        self.logger.info(f'Exporting selectivities vs. temperature data for CO2 hydrogenation reaction to "{output_data_path.joinpath("selectivity.dat")}"')
        if not output_data_path.exists():
            output_data_path.mkdir(parents=True)
        with output_data_path.joinpath('selectivity.dat').open(mode='w') as f:
            f.write(str(selectivity))

