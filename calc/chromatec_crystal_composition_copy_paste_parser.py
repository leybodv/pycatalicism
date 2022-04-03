from pathlib import Path

from .parser import Parser
from .rawdata import RawData
from .parserexception import ParserException
from ..logging_decorator import Logging

class ChromatecCrystalCompositionCopyPasteParser(Parser):
    """
    """

    @Logging
    def __init__(self):
        """
        """
        super().__init__()

    def parse_data(self, input_data_path:Path, initial_data_path:Path) -> RawData:
        """
        """
        if not initial_data_path.is_file():
            raise ParserException(f'initial data path {initial_data_path} must be a file')
        if not input_data_path.is_dir():
            raise ParserException(f'input data path {input_data_path} must be a directory')
        _, Cs_i, Ta_i, Pa_i, f_i = self._parse_file(initial_data_path)
        flow_is_measured = Ta_i and Pa_i and f_i
        Ts = []
        Cs_f = []
        Ta_f = [] if flow_is_measured else None
        Pa_f = [] if flow_is_measured else None
        f_f = [] if flow_is_measured else None
        for file in input_data_path.iterdir():
            if file == initial_data_path:
                continue
            if file.is_dir():
                self.logger.warning(f'Found directory {file} in input data path')
                continue
            try:
                T, C, Ta, Pa, f = self._parse_file(file)
            except ParserException:
                self.logger.warning(f'Wrong data format in file {file}. Skipping.')
                continue
            Ts.append(T)
            Cs_f.append(C)
            if Ta_f is not None and Pa_f is not None and f_f is not None:
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
            self.logger.debug(f'processing line: "{line}"')
            if line.startswith('Температура'):
                T = float(line.split(sep='\t')[1])
            if line.startswith('Название\tВремя. мин\tДетектор\tКонцентрация\tЕд. измерения\tПлощадь\tВысота'):
                while True:
                    if lines:
                        line = lines.pop(0)
                        if line == '':
                            break
                        self.logger.debug(f'processing line: "{line}"')
                        compound = line.split(sep='\t')[0]
                        concentration = line.split(sep='\t')[3]
                        C[compound] = float(concentration)
                    else:
                        break
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
        with path.open(mode='r') as file:
            contents = file.read()
            new_contents = contents.replace(',', '.')
        return new_contents
