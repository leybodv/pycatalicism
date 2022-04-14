from pycatalicism.calc.co2hydrogenationcalculator import CO2HydrogenationCalculator
from pycatalicism.calc.rawdata import RawData
from pycatalicism.calc.conversion import Conversion
from pycatalicism.logging_decorator import Logging

class CO2HydrogenationProductsBasisCalculator(CO2HydrogenationCalculator):
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
        self.logger.info(f'Calculating conversion for CO2 hydrogenation reaction based on reaction products')
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
        conversion = Conversion(temperatures, alphas)
        return conversion

    def _get_n(self, compound:str) -> int:
        """
        """
        n_str = compound[compound.find('C')+1]
        n = int(n_str) if n_str.isdecimal() else 1
        return n
