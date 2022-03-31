from pathlib import Path

from .plotter import Plotter
from .conversion import Conversion
from .selectivity import Selectivity

class COOxidationPlotter(Plotter):
    """
    """

    def plot(self, conversion:Conversion, selectivity:Selectivity|None, show_plot:bool=False, output_plot_path:Path|None=None):
        """
        """
        raise NotImplementedError()
