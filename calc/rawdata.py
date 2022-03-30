import numpy as np

class RawData():
    """
    Wrapper for imported data storage
    """

    def __init__(self, temperatures:list[float]|np.ndarray[float,np.dtype], initial_concentrations:dict[str,float], concentrations:np.ndarray[dict[str,float],np.dtype], initial_ambient_temperature:float|None=None, initial_ambient_pressure:float|None=None, initial_flow:float|None=None, final_ambient_temperatures:list[float]|np.ndarray[float,np.dtype]|None=None, final_ambient_pressures:list[float]|np.ndarray[float,np.dtype]|None=None, final_flows:list[float]|np.ndarray[float,np.dtype]|None=None):
        """
        """
        self.temperatures = np.array(temperatures)
        self.init_amb_temp = initial_ambient_temperature
        self.init_amb_pres = initial_ambient_pressure
        self.init_flow = initial_flow
        self.fin_amb_temps = None if final_ambient_temperatures is None else np.array(final_ambient_temperatures)
        self.fin_amb_pres = None if final_ambient_pressures is None else np.array(final_ambient_pressures)
        self.fin_flows = None if final_flows is None else np.array(final_flows)
        self.init_concs = initial_concentrations
        self.concs = concentrations

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
        return dict(self.concs[self.temperatures == temperature])[compound]
