import logging
from pathlib import Path

from . import logging_config
from .parser import Parser
from .rawdata import RawData

class ChromatecCrystalCompositionCopyPasteParser(Parser):
    """
    """

    def __init__(self):
        """
        """
        self.logger = logging.getLogger(__class__.__name__)
        logging_config.configure_logger(self.logger)
        self.logger.debug(f'creating {__class__.__name__}')

    def parse_data(self, input_data_path:Path, initial_data_path:Path) -> RawData:
        """
        """
        self.logger.debug(f'parsing data from {input_data_path}')
        if not initial_data_path.is_file():
            raise Exception(f'initial data path {initial_data_path} must be a file')
        if not input_data_path.is_dir():
            raise Exception(f'input data path {input_data_path} must be a directory')
        _, Cs_i, Ta_i, Pa_i, f_i = self._parse_file(initial_data_path)
        Ts = []
        Cs_f = []
        Ta_f = []
        Pa_f = []
        f_f = []
        for file in input_data_path.iterdir():
            if file == initial_data_path:
                continue
            T, C, Ta, Pa, f = self._parse_file(file)
            Ts.append(T)
            Cs_f.append(C)
            Ta_f.append(Ta)
            Pa_f.append(Pa)
            f_f.append(f)
        rawdata = RawData(temperatures=Ts, initial_concentrations=Cs_i, concentrations=Cs_f, initial_ambient_temperature=Ta_i, initial_ambient_pressure=Pa_i, initial_flow=f_i, final_ambient_temperatures=Ta_f, final_ambient_pressures=Pa_f, final_flows=f_f)
        return rawdata

    def _parse_file(self, path:Path) -> tuple[float,dict[str,float],float|None,float|None,float|None]:
        """
        """
        file_contents = self._replace_commas_with_dots(path)
        T = None
        C = {}
        Ta = None
        Pa = None
        f = None
        lines = file_contents.split(sep='\n')
        while lines:
            line = lines.pop(0)
            if line.startswith('Температура'):
                T = float(line.split(sep='\t')[1])
            if line.startswith('Название\tВремя. мин\tДетектор\tКонцентрация\tЕд. измерения\tПлощадь\tВысота'):
                while line != '' or lines:
                    line = lines.pop(0)
                    compound = line.split(sep='\t')[0]
                    concentration = line.split(sep='\t')[3]
                    C[compound] = float(concentration)
            if line.startswith('Темп. (газовые часы)'):
                Ta = float(line.split(sep='\t')[1])
            if line.startswith('Давление (газовые часы)'):
                Pa = float(line.split(sep='\t')[1])
            if line.startswith('Поток'):
                f = float(line.split(sep='\t')[1])
        if T is None or len(C) == 0:
            raise ParserException(f'Wrong data format in file {path}')
        return (T, C, Ta, Pa, f)

    def _replace_commas_with_dots(self, path:Path) -> str:
        """
        replace all commas with dots in a file

        parameters
        ----------
            path:Path
                path to file for processing

        returns
        -------
            new_contents:str
                string with file contents in which commas were replaced with dots
        """
        self.logger.debug('starting replace of commas with dots')
        with path.open(mode='r') as file:
            contents = file.read()
            new_contents = contents.replace(',', '.')
        self.logger.debug('finished replace of commas with dots')
        return new_contents
