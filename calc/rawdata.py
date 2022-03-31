import logging

import numpy as np

from . import logging_config

class RawData():
    """
    Wrapper for imported data storage
    """

    def __init__(self, temperatures:list[float]|np.ndarray[float,np.dtype], initial_concentrations:dict[str,float], concentrations:list[dict[str,float]]|np.ndarray[dict[str,float],np.dtype], initial_ambient_temperature:float|None=None, initial_ambient_pressure:float|None=None, initial_flow:float|None=None, final_ambient_temperatures:list[float]|np.ndarray[float,np.dtype]|None=None, final_ambient_pressures:list[float]|np.ndarray[float,np.dtype]|None=None, final_flows:list[float]|np.ndarray[float,np.dtype]|None=None):
        """
        """
        self.logger = logging.getLogger(__class__.__name__)
        logging_config.configure_logger(self.logger)
        self.temperatures = np.array(temperatures)
        self.init_amb_temp = initial_ambient_temperature
        self.init_amb_pres = initial_ambient_pressure
        self.init_flow = initial_flow
        self.logger.debug(f'{final_ambient_temperatures = }')
        self.fin_amb_temps = None if final_ambient_temperatures is None else np.array(final_ambient_temperatures)
        self.fin_amb_pres = None if final_ambient_pressures is None else np.array(final_ambient_pressures)
        self.fin_flows = None if final_flows is None else np.array(final_flows)
        self.init_concs = initial_concentrations
        self.concs = np.array(concentrations)

    def get_temperatures(self) -> np.ndarray[float, np.dtype]:
        """
        """
        return self.temperatures

    def get_init_amb_temp(self) -> float|None:
        """
        """
        return self.init_amb_temp

    def get_init_amb_pres(self) -> float|None:
        """
        """
        return self.init_amb_pres

    def get_init_flow(self) -> float|None:
        """
        """
        return self.init_flow

    def get_fin_amb_temp(self, temperature:float) -> float|None:
        """
        """
        self.logger.debug(f'{self.fin_amb_temps = }')
        if self.fin_amb_temps is not None:
            return float(self.fin_amb_temps[self.temperatures == temperature])
        else:
            return None

    def get_fin_amb_pres(self, temperature:float) -> float|None:
        """
        """
        if self.fin_amb_pres is not None:
            return float(self.fin_amb_pres[self.temperatures == temperature])
        else:
            return None

    def get_fin_flow(self, temperature:float) -> float|None:
        """
        """
        if self.fin_flows is not None:
            return float(self.fin_flows[self.temperatures == temperature])
        else:
            return None

    def get_init_conc(self, compound:str) -> float:
        """
        """
        return self.init_concs[compound]

    def get_conc(self, compound:str, temperature:float) -> float:
        """
        """
        self.logger.debug(f'{self.concs = }')
        self.logger.debug(f'{self.temperatures = }')
        self.logger.debug(f'{compound = }')
        self.logger.debug(f'{temperature = }')
        self.logger.debug(f'{self.concs[self.temperatures == temperature][0][compound] = }')
        try:
            conc = self.concs[self.temperatures == temperature][0][compound]
        except KeyError:
            self.logger.warning(f'Did not find concentration for "{compound}" at "{temperature}". Returning zero')
            conc = 0
        return conc
