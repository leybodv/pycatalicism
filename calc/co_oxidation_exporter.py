from pathlib import Path

from calc.exporter import Exporter
from calc.conversion import Conversion
from calc.selectivity import Selectivity
from calc.exporterexception import ExporterException
from logging_decorator import Logging

class COOxidationExporter(Exporter):
    """
    Class for exporting conversion data for CO oxidation reaction to conversion.dat to a directory provided by user of this class.
    """

    @Logging
    def __init__(self):
        """
        Registers logger with instances of this class which can be accessed via self.logger instance variable.
        """
        super().__init__()

    def export(self, output_data_path:Path, conversion:Conversion, selectivity:Selectivity|None):
        """
        Main interface of this class. Exports conversion data for CO oxidation reaction to conversion.dat to a directory provided by user of this method.

        parameters
        ----------
        output_data_path:Path
            path to directory to export resulting data
        conversion:Conversion
            wrapper of CO conversion at different temperatures
        selectivity:Selectivity|None
            should be None since selectivity does not make sense for CO oxidation reaction

        raises
        ------
        exception:ExporterException
            if ouput_data_path exists and not directory
        """
        if output_data_path.exists() and not output_data_path.is_dir():
            raise ExporterException(f'Data path for exporting data must be a folder')
        self._export_conversion(output_data_path, conversion)

    def _export_conversion(self, output_data_path:Path, conversion:Conversion):
        """
        Export CO conversion data to conversion.dat at output_data_path directory

        parameters
        ----------
        ouput_data_path:Path
            path to directory to export conversion data
        conversion:Conversion
            wrapper of CO conversion at different temperatures
        """
        self.logger.info(f'Exporting conversion vs. temperature data for CO oxidation reaction to "{output_data_path.joinpath("conversion.dat")}"')
        if not output_data_path.exists():
            output_data_path.mkdir(parents=True)
        with output_data_path.joinpath('conversion.dat').open(mode='w') as f:
            sorted_conversion = conversion.get_sorted()
            f.write(str(sorted_conversion))
