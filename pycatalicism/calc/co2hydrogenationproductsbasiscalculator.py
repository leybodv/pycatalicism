from pycatalicism.calc.co2hydrogenationcalculator import CO2HydrogenationCalculator
from pycatalicism.calc.rawdata import RawData
from pycatalicism.calc.conversion import Conversion
from pycatalicism.logging_decorator import Logging

class CO2HydrogenationProductsBasisCalculator(CO2HydrogenationCalculator):
    """
    Calculates CO2 conversion and CO, alkanes selectivity at different temperatures from parsed data for CO2 hydrogenation reaction based on products composition
    """

    @Logging
    def __init__(self):
        """
        Registers logger with the object which can be accessed via self.logger instance variable
        """
        super().__init__()

    def calculate_conversion(self, input_data:RawData) -> Conversion:
        """
        Calculates CO2 conversion at different temperatures for CO2 hydrogenation reaction based on products concentrations.

        CO2 conversion is calculated as:

        a = (SUM(nj * Cj) / C(CO2)i) * ((pf * ff * Ti) / (pi * fi * Tf))
        where
            nj - stoichiometric coefficient for jth product
                CO2 + H2 = CO + H2O, n = 1
                CO2 + 4H2 = CH4 + 2H2O, n = 1
                2CO2 + 7H2 = C2H6 + 4H2O, n = 2
                3CO2 + 10H2 = C3H8 + 6H2O, n = 3
                4CO2 + 13H2 = C4H10 + 8H2O, n = 4
                5CO2 + 16H2 = C5H12 + 10H2O, n = 5
            Cj - concentration of jth product in mol.%
            fi, ff - total gas flow rates before and after catalytic reactor, respectively, in m^3/s
            pi, pf - pressure of gas at point of total gas flow rate measurement before and after catalytic reactor, respectively, in Pa
            Ti, Tf - temperature of gas at point of total gas flow rate measurement before and after catalytic reactor, respectively, in K

        If flow rate measurement data is not provided, conversion is calculated based solely on concentrations and warning is logged to console in this case.

        parameters
        ----------
        input_data:RawData
            wrapper of parsed data containing product concentrations at different temperatures as well as initial CO2 concentration before reaction started

        returns
        -------
        conversion:Conversion
            wrapper with CO2 conversion at different temperatures data
        """
        self.logger.warning(f'Calculating conversion for CO2 hydrogenation reaction based on reaction products')
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
            if T_i is None or p_i is None or f_i is None or T_f is None or p_f is None or f_f is None:
                self.logger.warning(f'No data about initial and final flow rate found. Calculating results based only on concentrations')
                T_i = 1
                p_i = 1
                f_i = 1
                T_f = 1
                p_f = 1
                f_f = 1
            product_sum = 0
            for compound in ['CO', 'CH4', 'C2H6', 'C3H8', 'i-C4H10', 'n-C4H10', 'i-C5H12', 'n-C5H12']:
                n = self._get_n(compound)
                product_sum = product_sum + n * input_data.get_conc(compound, temperature)
            alpha = (product_sum / C_CO2_i) * ((p_f * f_f * T_i) / (p_i * f_i * T_f))
            temperatures.append(temperature)
            alphas.append(alpha)
        conversion = Conversion(temperatures, alphas, input_data.get_sample_name())
        return conversion

    def _get_n(self, compound:str) -> int:
        """
        Get stoichiometry coefficient in CO2 hydrogenation reaction for specified compound.

        parameters
        ----------
        compound:str
            compound to calculate stoichiometry coefficient for

        returns
        -------
        n:int
            stoichiometry coefficient
        """
        n_str = compound[compound.find('C')+1]
        n = int(n_str) if n_str.isdecimal() else 1
        return n
