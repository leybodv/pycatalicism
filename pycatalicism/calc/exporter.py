from pathlib import Path

from pycatalicism.calc.conversion import Conversion
from pycatalicism.calc.selectivity import Selectivity

class Exporter():
    """
    Abstract class. Concrete instances of child classes are intended for exporting calculated by the program data
    """

    def export(self, output_data_path:Path, conversion:Conversion|None, selectivity:Selectivity|None):
        """
        Concrete classes should override this method to export results of calculations.

        parameters
        ----------
        output_data_path:Path
            path to directory to export resulting data
        conversion:Conversion
            wrapper with conversion vs. temperature data
        selectivity:Selectivity|None
            wrapper with selectivity vs. temperature data or None if selectivity does not make sensefor reaction under consideration

        raises
        ------
        exception:NotImplementedError
            if this method is not overriden
        """
        raise NotImplementedError()
