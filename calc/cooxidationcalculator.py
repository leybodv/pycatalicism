import logging

from . import logging_config
from .calculator import Calculator
from .rawdata import RawData
from .conversion import Conversion

class COOxidationCalculator(Calculator):
    """
    """

    def __init__(self):
        """
        """
        self.logger = logging.getLogger(__class__.__name__)
        logging_config.configure_logger(self.logger)
        self.logger.debug(f'creating {__class__.__name__}')

    def calculate_conversion(self, input_data:RawData) -> Conversion:
        """
        raise warning about wrong calculation
        """
        self.logger.debug(f'calculatong conversion')
        temperatures = []
        alphas = []
        for temperature in input_data.get_temperatures():
            T_i = input_data.get_init_amb_temp()
            p_i = input_data.get_init_amb_pres()
            f_i = input_data.get_init_flow()
            T_f = input_data.get_fin_amb_temp(temperature)
            p_f = input_data.get_fin_amb_pres(temperature)
            f_f = input_data.get_fin_flow(temperature)
            C_CO_i = input_data.get_init_conc('CO')
            C_CO_f = input_data.get_conc('CO', temperature)
            if T_i == None or p_i == None or f_i == None or T_f == None or p_f == None or f_f == None:
                T_i = 1
                p_i = 1
                f_i = 1
                T_f = 1
                p_f = 1
                f_f = 1
            alpha = (C_CO_i - C_CO_f) / C_CO_i
            temperatures.append(temperature)
            alphas.append(alpha)
        conversion = Conversion(temperatures, alphas)
        return conversion

    def calculate_selectivity(self, input_data:RawData) -> None:
        """
        """
        self.logger.debug('nothing to calculate')
        return None
