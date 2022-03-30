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
        if self._data_file_format_is_ok(initial_data_path):
            _, Cs_i, Ta_i, Pa_i, f_i = self._parse_file(initial_data_path)
        else:
            raise Exception(f'Wrong format in file {initial_data_path} with initial data')
        Ts = []
        Cs_f = []
        Ta_f = []
        Pa_f = []
        f_f = []
        if not input_data_path.is_dir():
            raise Exception(f'input data path {input_data_path} must be a directory')
        for file in input_data_path.iterdir():
            if self._data_file_format_is_ok(file):
                T, C, Ta, Pa, f = self._parse_file(file)
                Ts.append(T)
                Cs_f.append(C)
                Ta_f.append(Ta)
                Pa_f.append(Pa)
                f_f.append(f)
        rawdata = RawData(temperatures=Ts, initial_concentrations=Cs_i, concentrations=Cs_f, initial_ambient_temperature=Ta_i, initial_ambient_pressure=Pa_i, initial_flow=f_i, final_ambient_temperatures=Ta_f, final_ambient_pressures=Pa_f, final_flows=f_f)
        return rawdata

    def _data_file_format_is_ok(self, path:Path) -> bool:
        """
        """
        if path.is_file():
            temp_h = False
            conc_h = False
            with path.open(mode='r') as file:
                for line in file.readlines():
                    if line.startswith('Температура'):
                        temp_h = True
                    elif line.startswith('Название\tВремя, мин\tДетектор\tКонцентрация\tЕд, измерения\tПлощадь\tВысота'):
                        conc_h = True
            format_is_ok = temp_h and conc_h
        else:
            self.logger.warning(f'Path to data file {path} is not a file, skipping')
            format_is_ok = False
        if not format_is_ok:
            self.logger.warning(f'Data file format in {path} is wrong, skipping')
        return format_is_ok

    def _parse_file(self, path:Path) -> tuple[float,dict[str,float],float|None,float|None,float|None]:
        """
        """
        raise NotImplementedError()
