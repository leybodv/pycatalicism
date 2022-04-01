import logging

from . import logging_config
from .calculator import Calculator
from .rawdata import RawData
from .conversion import Conversion
from .selectivity import Selectivity

class CO2HydrogenationCalculator(Calculator):
    """
    """

    def __init__(self):
        """
        """
        self.logger = logging.getLogger(__class__.__name__)
        logging_config.configure_logger(self.logger)

    def calculate_conversion(self, input_data:RawData) -> Conversion:
        """
        """
        self.logger.info(f'Calculating conversion for CO2 hydrogenation reaction')
        temperatures = []
        alphas = []
        for temperature in input_data.get_temperatures():
            T_i = input_data.get_init_amb_temp()
            p_i = input_data.get_init_amb_pres()
            f_i = input_data.get_init_flow()
            T_f = input_data.get_fin_amb_temp(temperature)
            p_f = input_data.get_fin_amb_pres(temperature)
            f_f = input_data.get_fin_flow(temperature)
            C_CO2_i = input_data.get_init_conc('CO2')
            C_CO2_f = input_data.get_conc('CO2', temperature)
            if T_i is None or p_i is None or f_i is None or T_f is None or p_f is None or f_f is None:
                self.logger.warning(f'No data about initial and final flow rate found. Calculating results based only on concentrations')
                T_i = 1
                p_i = 1
                f_i = 1
                T_f = 1
                p_f = 1
                f_f = 1
            alpha = ((p_i * f_i / T_i) * C_CO2_i - (p_f * f_f / T_f) * C_CO2_f) / (p_i * f_i / T_i) * C_CO2_i
            temperatures.append(temperature)
            alphas.append(alpha)
        conversion = Conversion(temperatures, alphas)
        return conversion

    def calculate_selectivity(self, input_data:RawData) -> Selectivity:
        """
        """
        self.logger.info(f'Calculating selectivities for CO2 hydrogenation reaction')
        temperatures = []
        s_list = []
        for temperature in input_data.get_temperatures():
            c_tot = 0
            s_dict = {}
            for compound in ['CO', 'CH4', 'C2H6', 'C3H8', 'i-C4H10', 'n-C4H10', 'i-C5H12', 'n-C5H12']:
                s_dict[compound] = input_data.get_conc(compound, temperature)
                c_tot = c_tot + s_dict[compound]
            for key in s_dict:
                s_dict[key] = s_dict[key] / c_tot
            temperatures.append(temperature)
            s_list.append(s_dict)
        selectivity = Selectivity(temperatures, s_list)
        return selectivity
