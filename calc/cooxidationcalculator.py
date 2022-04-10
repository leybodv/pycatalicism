from pycatalicism.calc.calculator import Calculator
from pycatalicism.calc.rawdata import RawData
from pycatalicism.calc.conversion import Conversion
from pycatalicism.logging_decorator import Logging

class COOxidationCalculator(Calculator):
    """
    Class for calculating CO conversion data.
    """

    @Logging
    def __init__(self):
        """
        Registers logger with instance of this class which can be accessed via self.logger instance variable.
        """
        super().__init__()

    def calculate_conversion(self, input_data:RawData) -> Conversion:
        """
        Main interface to this class. Calculate CO conversion at different temperatures for CO oxidation reaction. Conversion is calculated as:

        a = ((pi * fi / Ti) * C(CO)i - (pf * ff / Tf) * C(CO)f) /  ((pi * fi / Ti) * C(CO)i)
        where
            C(CO)i, C(CO)f - concentrations of CO before and after catalytic reactor, respectively, in mol.%
            fi, ff - total gas flow rates before and after catalytic reactor, respectively, in m^3/s
            pi, pf - pressure of gas at point of total gas flow rate measurement before and after catalytic reactor, respectively, in Pa
            Ti, Tf - temperature of gas at point of total gas flow rate measurement before and after catalytic reactor, respectively, in K

        If flow rate measurement data is not provided, conversion is calculated based solely on CO concentrations and warning is logged to console in this case.

        parameters
        ----------
        input_data:RawData
            wrapper with concentrations and flow rate data

        returns
        -------
        conversion:Conversion
            wrapper with conversion vs. temperature data
        """
        self.logger.info(f'Calculating conversion for CO oxidation reaction')
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
            if T_i is None or p_i is None or f_i is None or T_f is None or p_f is None or f_f is None:
                self.logger.warning(f'No data about initial and final flow rate found. Calculating results based only on concentrations')
                T_i = 1
                p_i = 1
                f_i = 1
                T_f = 1
                p_f = 1
                f_f = 1
            alpha = ((p_i * f_i / T_i) * C_CO_i - (p_f * f_f / T_f) * C_CO_f) / (p_i * f_i / T_i) * C_CO_i
            temperatures.append(temperature)
            alphas.append(alpha)
        conversion = Conversion(temperatures, alphas)
        return conversion

    def calculate_selectivity(self, input_data:RawData) -> None:
        """
        Overrides method of superclass. Just returns None since selectivity for CO oxidation reaction does not make sense.
        """
        return None
