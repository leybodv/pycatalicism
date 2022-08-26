from calc.calculator import Calculator
from calc.rawdata import RawData
from calc.conversion import Conversion
from calc.selectivity import Selectivity
from logging_decorator import Logging

class CO2HydrogenationCalculator(Calculator):
    """
    Calculates CO2 conversion and CO, alkanes selectivity at different temperatures from parsed data for CO2 hydrogenation reaction
    """

    @Logging
    def __init__(self):
        """
        Registers logger with the object which can be accessed via self.logger instance variable
        """
        super().__init__()

    def calculate_conversion(self, input_data:RawData) -> Conversion:
        """
        Calculates CO2 conversion at different temperatures for CO2 hydrogenation reaction.

        CO2 conversion is calculated as:

        a = ((pi * fi / Ti) * C(CO2)i - (pf * ff / Tf) * C(CO2)f) /  ((pi * fi / Ti) * C(CO2)i)
        where
            C(CO2)i, C(CO2)f - concentrations of CO2 before and after catalytic reactor, respectively, in mol.%
            fi, ff - total gas flow rates before and after catalytic reactor, respectively, in m^3/s
            pi, pf - pressure of gas at point of total gas flow rate measurement before and after catalytic reactor, respectively, in Pa
            Ti, Tf - temperature of gas at point of total gas flow rate measurement before and after catalytic reactor, respectively, in K

        If flow rate measurement data is not provided, conversion is calculated based solely on CO2 concentrations and warning is logged to console in this case.

        parameters
        ----------
        input_data:RawData
            wrapper of parsed data containing CO2 concentrations at different temperatures as well as initial CO2 concentration before reaction started

        returns
        -------
        conversion:Conversion
            wrapper with CO2 conversion at different temperatures data
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
        conversion = Conversion(temperatures, alphas, input_data.get_sample_name())
        return conversion

    def calculate_selectivity(self, input_data:RawData) -> Selectivity:
        """
        Calculates selectivity to CO, CH4, C2H6, C3H8, i-C4H10, n-C4H10, i-C5H12, n-C5H12 at different temperatures from compounds concentrations.

        Selectivity to i-th component is calculated as:

        Si = Xi * n / SUM(Xi * n)
        where
            Xi - concentration of ith component in mol.%
            n - stoichiometry coefficient in CO2 hydrogenation reaction
                CO2 + H2 = CO + H2O, n = 1
                CO2 + 4H2 = CH4 + 2H2O, n = 1
                2CO2 + 7H2 = C2H6 + 4H2O, n = 2
                3CO2 + 10H2 = C3H8 + 6H2O, n = 3
                4CO2 + 13H2 = C4H10 + 8H2O, n = 4
                5CO2 + 16H2 = C5H12 + 10H2O, n = 5

        parameters
        ----------
        input_data:RawData
            wrapper with concentrations of reaction product compounds at different temperatures

        returns
        -------
        selectivity:Selectivity
            wrapper with selectivities to corresponding compounds at different temperatures
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
        selectivity = Selectivity(temperatures, s_list, input_data.get_sample_name())
        return selectivity
