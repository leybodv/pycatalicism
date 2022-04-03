from pathlib import Path

import matplotlib.pyplot as plt

from .plotter import Plotter
from .plotterexception import PlotterException
from .conversion import Conversion
from .selectivity import Selectivity
from ..logging_decorator import Logging

class COOxidationPlotter(Plotter):
    """
    """

    @Logging
    def __init__(self):
        """
        """

    def plot(self, conversion:Conversion, selectivity:Selectivity|None, show_plot:bool=False, output_plot_path:Path|None=None):
        """
        """
        fig, ax = plt.subplots()
        sorted_conversion = conversion.get_sorted()
        ax.plot(sorted_conversion.get_temperatures(), sorted_conversion.get_alphas(), marker='o', markersize=5)
        ax.set_ylim(bottom=-0.1, top=1.1)
        ax.set_xlabel('Temperature, °C')
        ax.set_ylabel('$\mathrm{CO}$ conversion')
        if show_plot:
            self.logger.info(f'Plotting conversion vs. temperature for CO oxidation reaction')
            plt.show()
        if output_plot_path:
            if output_plot_path.exists() and not output_plot_path.is_dir():
                raise PlotterException(f'Output plot path must be a directory')
            if not output_plot_path.exists():
                output_plot_path.mkdir(parents=True)
            self.logger.info(f'Exporting plot of conversion vs. temperature for CO oxidation reaction')
            dpi = 300
            width = 80 / 25.4
            height = 80 / 25.4
            fig.set_dpi(dpi)
            fig.set_figheight(height)
            fig.set_figwidth(width)
            fig.set_tight_layout(True)
            fig.savefig(fname=output_plot_path.joinpath('result.png'))
