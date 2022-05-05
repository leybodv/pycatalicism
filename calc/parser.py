from pathlib import Path

from pycatalicism.calc.rawdata import RawData

class Parser():
    """
    Abstract class for parsers of initial data.
    """

    def parse_data(self, input_data_path:Path, initial_data_path:Path, sample_name:str|None) -> RawData:
        """
        Methods of concrete classes should override this method.

        parameters
        ----------
        input_data_path:Path
            path to directory with data files
        initial_data_path:Path
            path to file with initial (i.e. before catalytic reaction occured) dad
        sample_name:str|None
            name of sample used as label for plotting

        returns
        -------
        raw_data:RawData
            wrapper with parsed data

        raises
        ------
        exception:NotImplementedError
            if this method is not overriden
        """
        raise NotImplementedError()
