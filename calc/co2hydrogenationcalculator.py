from pycatalicism.calc.calculator import Calculator
from pycatalicism.calc.rawdata import RawData
from pycatalicism.calc.conversion import Conversion
from pycatalicism.calc.selectivity import Selectivity
from pycatalicism.logging_decorator import Logging

class CO2HydrogenationCalculator(Calculator):
    """
    """

    @Logging
    def __init__(self):
        """
        """
        super().__init__()

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
            self.logger.debug(f'{temperature = }')
            self.logger.debug(f'{C_CO2_i = }')
            self.logger.debug(f'{C_CO2_f = }')
            if T_i is None or p_i is None or f_i is None or T_f is None or p_f is None or f_f is None:
                self.logger.warning(f'No data about initial and final flow rate found. Calculating results based only on concentrations')
                T_i = 1
                p_i = 1
                f_i = 1
                T_f = 1
                p_f = 1
                f_f = 1
            alpha = ((p_i * f_i / T_i) * C_CO2_i - (p_f * f_f / T_f) * C_CO2_f) / ((p_i * f_i / T_i) * C_CO2_i)
            self.logger.debug(f'{alpha = }')
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
            self.logger.debug(f'{temperature = }')
            c_tot = 0
            s_dict = {}
            for compound in ['CO', 'CH4', 'C2H6', 'C3H8', 'i-C4H10', 'n-C4H10', 'i-C5H12', 'n-C5H12']:
                n_str = compound[compound.find('C')+1]
                n = int(n_str) if n_str.isdecimal() else 1
                s_dict[compound] = input_data.get_conc(compound, temperature) * n
                c_tot = c_tot + s_dict[compound]
                self.logger.debug(f'{compound = }')
                self.logger.debug(f'{n = }')
                self.logger.debug(f'{input_data.get_conc(compound, temperature) = }')
            self.logger.debug(f'{s_dict = }')
            self.logger.debug(f'{sum(list(s_dict.values())) = }')
            self.logger.debug(f'{c_tot = }')
            if c_tot == 0:
                c_tot = 1
            for key in s_dict:
                s_dict[key] = s_dict[key] / c_tot
            self.logger.debug(f'{s_dict = }')
            self.logger.debug(f'{sum(list(s_dict.values())) = }')
            temperatures.append(temperature)
            s_list.append(s_dict)
        selectivity = Selectivity(temperatures, s_list)
        return selectivity
