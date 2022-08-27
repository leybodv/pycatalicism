from pathlib import Path

import matplotlib.pyplot as plt

from calc.plotter import Plotter
from calc.plotterexception import PlotterException
from calc.conversion import Conversion
from calc.selectivity import Selectivity
from logger.logging_decorator import Logging

class COOxidationPlotter(Plotter):
    """
    Class for plotting CO oxidation conversion data and exporting resulting plots to file.
    """

    @Logging
    def __init__(self):
        """
        Registers logger with instances of this class which can be accessed via self.logger instance variable
        """

    def plot(self, conversion:Conversion, selectivity:Selectivity|None, show_plot:bool=False, output_plot_path:Path|None=None):
        """
        Main interface of this class. Plots conversion vs. temperature as line plot. If show_plot is true, shows plots. If output_data_path was provided, exports plots to result.png to provided directory

        parameters
        ----------
        conversion:Conversion
            wrapper for CO conversion at different temperatures data
        selectivity:Selectivity|None
            should be None since selectivity does not make sense for CO oxidation
        show_plot:bool (default:False)
            if True, show plots
        output_data_path:Path|None (default:None)
            path to directory to export data
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
