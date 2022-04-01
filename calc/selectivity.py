import logging

import numpy as np

from . import logging_config

class Selectivity():
    """
    Wrapper for selectivity data storage
    """

    def __init__(self, temperatures:list[float], selectivities:list[dict[str,float]]):
        """
        """
        self.logger = logging.getLogger(__class__.__name__)
        logging_config.configure_logger(self.logger)
        self.logger.warning(f'{self.logger.getEffectiveLevel() = }')
        self.temperatures = np.array(temperatures)
        self.selectivities = np.array(selectivities)

    def __str__(self) -> str:
        """
        """
        sorted_selectivities = self.get_sorted()
        c_l = []
        for compound in sorted_selectivities.get_selectivities()[0]:
            c_l.append(compound)
        header = 'Temperature'
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
        """
        return self.temperatures

    def get_selectivities(self) -> np.ndarray[dict[str,float], np.dtype]:
        """
        """
        return self.selectivities

    def get_selectivity(self, compound:str, temperature:float) -> float:
        """
        """
        self.logger.debug(f'{self.get_selectivities() = }')
        self.logger.debug(f'{self.get_selectivities()[self.get_temperatures()==temperature] = }')
        return self.get_selectivities()[self.temperatures==temperature][compound]

    def get_sorted(self) -> 'Selectivity':
        """
        """
        zipped_lists = zip(self.get_temperatures(), self.get_selectivities(), strict=True)
        sorted_pairs = sorted(zipped_lists)
        tuples = zip(*sorted_pairs)
        sorted_temperatures, sorted_selectivities = [list(tuple) for tuple in tuples]
        return Selectivity(sorted_temperatures, sorted_selectivities)

    def get_selectivities_at(self, temperature:float) -> dict[str,float]:
        """
        """
        return self.get_selectivities()[self.get_temperatures() == temperature]
