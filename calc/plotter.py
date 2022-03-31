from pathlib import Path

from .conversion import Conversion
from .selectivity import Selectivity

class Plotter():
    """
    Abstract class
    """

    def plot(self, conversion:Conversion, selectivity:Selectivity|None, show_plot:bool=False, output_plot_path:Path|None=None):
        """
        """
        raise NotImplementedError()
