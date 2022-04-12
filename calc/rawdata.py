import numpy as np

from pycatalicism.logging_decorator import Logging

class RawData():
    """
    Wrapper for imported data storage. Data are stored as numpy.ndarrays.
    """

    @Logging
    def __init__(self, temperatures:list[float]|np.ndarray[float,np.dtype], initial_concentrations:dict[str,float], concentrations:list[dict[str,float]]|np.ndarray[dict[str,float],np.dtype], initial_ambient_temperature:float|None=None, initial_ambient_pressure:float|None=None, initial_flow:float|None=None, final_ambient_temperatures:list[float]|np.ndarray[float,np.dtype]|None=None, final_ambient_pressures:list[float]|np.ndarray[float,np.dtype]|None=None, final_flows:list[float]|np.ndarray[float,np.dtype]|None=None):
        """
        Registers logger with instance of this class which can be accessed via self.logger instance variable. Assigns parameters to instance variables converting lists to numpy.ndarray types.

        parameters
        ----------
        temperatures:list[float]|numpy.ndarray[float]
            list of temperatures at which gas composition measurements were done
        initial_concentrations:dict[str,float]
            dictionary of initial concentrations (i.e. before reaction started) of catalytic reaction compounds in a format {<compound>:<concentration>}
                compound:str
                    chemical formula of compound
                concentration:float
                    concentration in mol.%
        concentrations:list[dict[str,float]]|numpy.ndarray[dict[str,float]]
            list of compounds concentrations parrallel to temperatures list. Each list element is a dictionary in a format similar to initial_concentrations parameter
        initial_ambient_temperature:float|None (default:None)
            temperature of gas at the point of initial total flow rate measurement in °C
        initial_ambient_pressure:float|None (default:None)
            pressure of gas at the point of initial total flow rate measurement in Pa
        initial_flow:float|None (default:None)
            initial total flow rate in ml/min
        final_ambient_temperatures:list[float]|numpy.ndarray[float]|None (default:None)
            list of temperatures of gas at the point of total flow rate measurement in °C
        final_ambient_pressures:list[float]|numpy.ndarray[float]|None (default:None)
            list of pressures of gas at the point of total flow rate measurement in Pa
        final_flows:list[float]|numpy.ndarray[float]|None (default:None)
            list of total flow rates in ml/min
        """
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
        Get list of temperatures at which gas composition measurements were done

        returns
        -------
        temperatures:numpy.ndarray[float]
            list of temperatures
        """
        return self.temperatures

    def get_init_amb_temp(self) -> float|None:
        """
        Get temperature of gas at the point of initial total flow rate measurement in °C

        returns
        -------
        temperature:float|None
            temperature value in °C
        """
        return self.init_amb_temp

    def get_init_amb_pres(self) -> float|None:
        """
        Get pressure of gas at the point of initial total flow rate measurement in Pa

        returns
        -------
        pressure:float|None
            pressure in Pa
        """
        return self.init_amb_pres

    def get_init_flow(self) -> float|None:
        """
        Get initial total flow rate in ml/min

        returns
        -------
        flow_rate:float|None
            initial total flow rate in ml/min
        """
        return self.init_flow

    def get_fin_amb_temp(self, temperature:float) -> float|None:
        """
        Get temperature of gas at the point of total flow rate measurement during catalytic experiment at temperature provided as parameter to the method

        parameters
        ----------
        temperature:float
            temperature of catalytic experiment

        returns
        -------
        ambient_temperature:float|None
            temperature in °C
        """
        self.logger.debug(f'{self.fin_amb_temps = }')
        if self.fin_amb_temps is not None:
            return float(self.fin_amb_temps[self.temperatures == temperature])
        else:
            return None

    def get_fin_amb_pres(self, temperature:float) -> float|None:
        """
        Get pressure of gas at the point of total flow rate measurement during catalytic experiment at temperature provided as parameter to the method

        parameters
        ----------
        temperature:float
            temperature of catalytic reaction at the measurement moment

        returns
        -------
        ambient_pressure:float|None
            pressure in Pa
        """
        if self.fin_amb_pres is not None:
            return float(self.fin_amb_pres[self.temperatures == temperature])
        else:
            return None

    def get_fin_flow(self, temperature:float) -> float|None:
        """
        Get total gas flow rate during catalytic reaction at temperature provided as parameter to the method

        parameters
        ----------
        temperature:float
            temperature of catalytic reaction at the measurement moment

        returns
        -------
        flow_rate:float|None
            flow rate in ml/min
        """
        if self.fin_flows is not None:
            return float(self.fin_flows[self.temperatures == temperature])
        else:
            return None

    def get_init_conc(self, compound:str) -> float:
        """
        Get initial concentration of compound

        parameters
        ----------
        compound:str
            compound to get initial concentration for

        returns
        -------
        initial_concentration:float
            initial concentration in mol.%
        """
        return self.init_concs[compound]

    def get_conc(self, compound:str, temperature:float) -> float:
        """
        Get concentration of compound at temperature of catalytic reaction provided as parameter to the method

        parameters
        ----------
        compound:str
            compound to get concentration for
        temperature:float
            temperature of catalytic reaction at which concentration was measured

        returns
        -------
        concentration:float
            concentration in mol.% or 0 if at specified temperature concentration for the compound is not found
        """
        self.logger.debug(f'{self.concs = }')
        self.logger.debug(f'{self.temperatures = }')
        self.logger.debug(f'{compound = }')
        self.logger.debug(f'{temperature = }')
        try:
            conc = self.concs[self.temperatures == temperature][0][compound]
        except KeyError:
            self.logger.warning(f'Did not find concentration for "{compound}" at "{temperature}". Returning zero')
            conc = 0
        return conc
