class Selectivity():
    """
    Wrapper for selectivity data storage
    """

    def __init__(self, temperatures:list[float], selectivities:list[dict[str,float]]):
        """
        """
        self.temperatures = temperatures
        self.selectivities = selectivities

    def __str__(self) -> str:
        """
        """
        sorted_selectivities = self._get_sorted()
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
