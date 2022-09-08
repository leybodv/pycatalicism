from pathlib import Path

from pycatalicism.calc.conversion import Conversion
from pycatalicism.calc.selectivity import Selectivity

class Plotter():
    """
    Abstract class for plotting resulting data
    """

    def plot(self, conversion:Conversion, selectivity:Selectivity|None, show_plot:bool=False, output_plot_path:Path|None=None, plot_title:str|None=None):
        """
        Method should be overriden by concrete classes. Plots conversion, selectivity vs. temperature plots, shows them and exports to file.

        parameters
        ----------
        conversion:Conversion
            wrapper for conversion data
        selectivity:Selectivity|None
            wrapper for selectivity data or None if selectivity does not make sense for reaction
        show_plot:bool (default:False)
            show plot if True
        output_plot_path:Path|None (default:None)
            path to directory to export resulting plots or None if export is not needed

        raises
        ------
        NotImplementedError
            if method is not overriden
        """
        raise NotImplementedError()
