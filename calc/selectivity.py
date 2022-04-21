import numpy as np

class Selectivity():
    """
    Wrapper for selectivity data storage. Selectivities are stored as numpy.ndarray of dictionaries, containing name of compounds and corresponding calculated selectivities. The list is parallel to the list of corresponding temperatures.
    """

    def __init__(self, temperatures:list[float]|np.ndarray[float, np.dtype], selectivities:list[dict[str,float]]|np.ndarray[dict[str,float], np.dtype], sample_name:str|None):
        """
        Assigns parameters to instance variables, converting lists to numpy.ndarrays.

        parameters
        ----------
        temperatures:list[float]|numpy.ndarray[float]
            list of temperatures of catalytic reaction at which measurements were done
        selectivities:list[dict[str,float]]|numpy.ndarray[dict[str,float]]
            list of dictionaries with selectivities parallel to temperatures list. Selectivities are stored in a format {<compound>:<selectivity>}
                compound:str
                    chemical formula of compound
                selectivity:float
                    selectivity of catalyst to this compound
        sample_name:str|None
            name of sample
        """
        self.temperatures = np.array(temperatures)
        self.selectivities = np.array(selectivities)
        self.sample_name = sample_name

    def __str__(self) -> str:
        """
        Get string representation of selectivities in a form of table:

        Temperature<tab>Selectivity

        returns
        -------
        string:str
            string representation of selectivities
        """
        sorted_selectivities = self.get_sorted()
        c_l = []
        for compound in sorted_selectivities.get_selectivities()[0]:
            c_l.append(compound)
        header = f'Sample\t{self.sample_name}\n\nTemperature'
        for compound in c_l:
            header = header + f'\t{compound}'
        header = header + '\n'
        data = ''
        for temperature in sorted_selectivities.get_temperatures():
            data = data + f'{temperature}'
            for compound in c_l:
                data = data + f'\t{sorted_selectivities.get_selectivity(compound, temperature)}'
            data = data + '\n'
        string = header + data
        return string

    def get_temperatures(self) -> np.ndarray[float, np.dtype]:
        """
        Get list of temperatures of catalytic reaction at which measurements were done

        returns
        -------
        temperatures:numpy.ndarray[float]
            list of temperatures
        """
        return self.temperatures

    def get_selectivities(self) -> np.ndarray[dict[str,float], np.dtype]:
        """
        Get list of selectivities calculated by the program

        returns
        -------
        selectivities:numpy.ndarray[dict[str,float]]
            list of selectivities
        """
        return self.selectivities

    def get_selectivity(self, compound:str, temperature:float) -> float:
        """
        Get selectivity of catalyst to compound at temperature of catalytic reaction provided as parameter to the method

        parameters
        ----------
        compound:str
            compound for which selectivity to return
        temperature:float
            temperature of catalytic reaction

        returns
        -------
        selectivity:float
            selectivity to specified compound
        """
        return self.get_selectivities()[self.temperatures==temperature][0][compound]

    def get_sorted(self) -> 'Selectivity':
        """
        Get selectivity object with temperatures and selectivities lists sorted in parallel based on temperatures

        returns
        -------
        selectivity:Selectivity
            sorted selectivity
        """
        zipped_lists = zip(self.get_temperatures(), self.get_selectivities(), strict=True)
        sorted_pairs = sorted(zipped_lists)
        tuples = zip(*sorted_pairs)
        sorted_temperatures, sorted_selectivities = [list(tuple) for tuple in tuples]
        return Selectivity(sorted_temperatures, sorted_selectivities)

    def get_selectivities_at(self, temperature:float) -> dict[str,float]:
        """
        Get selectivities at temperature of catalytic reaction provided as parameter to the method

        parameters
        ----------
        temperature:float
            temperature of catalytic reaction

        returns
        -------
        selectivities:dict[str,float]
            dictionary of selectivities at specified temperature
        """
        return self.get_selectivities()[self.get_temperatures() == temperature][0]
