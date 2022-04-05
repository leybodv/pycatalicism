from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.axes

from pycatalicism.calc.plotter import Plotter
from pycatalicism.calc.plotterexception import PlotterException
from pycatalicism.calc.conversion import Conversion
from pycatalicism.calc.selectivity import Selectivity
from pycatalicism.logging_decorator import Logging

class CO2HydrogenationPlotter(Plotter):
    """
    """

    @Logging
    def __init__(self):
        """
        """
        super().__init__()

    def plot(self, conversion:Conversion, selectivity:Selectivity, show_plot:bool=False, output_plot_path:Path|None=None):
        """
        """
        fig, (ax_conversion, ax_selectivity) = plt.subplots(nrows=1, ncols=2)
        ax_conversion = self._plot_conversion(ax_conversion, conversion)
        ax_selectivity = self._plot_selectivity(ax_selectivity, selectivity)
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
            width = 160 / 25.4
            height = 80 / 25.4
            fig.set_dpi(dpi)
            fig.set_figheight(height)
            fig.set_figwidth(width)
            fig.set_tight_layout(True)
            fig.savefig(fname=output_plot_path.joinpath('result.png'))

    def _plot_conversion(self, ax:matplotlib.axes.Axes, conversion:Conversion) -> matplotlib.axes.Axes:
        """
        """
        sorted_conversion = conversion.get_sorted()
        ax.plot(sorted_conversion.get_temperatures(), sorted_conversion.get_alphas(), marker='o', markersize=5)
        ax.set_ylim(bottom=-0.1, top=1.1)
        ax.set_xlabel('Temperature, °C')
        ax.set_ylabel('$\mathrm{CO_2}$ conversion')
        return ax

    def _plot_selectivity(self, ax:matplotlib.axes.Axes, selectivity:Selectivity) -> matplotlib.axes.Axes:
        """
        """
        sorted_selectivity = selectivity.get_sorted()
        s_dict = {}
        for temperature in sorted_selectivity.get_temperatures():
            for compound in sorted_selectivity.get_selectivities_at(temperature):
                self.logger.debug(f'{compound = }')
                self.logger.debug(f'{s_dict = }')
                if compound in s_dict:
                    self.logger.debug(f'{sorted_selectivity.get_selectivity(compound, temperature) = }')
                    s_dict[compound].append(sorted_selectivity.get_selectivity(compound, temperature))
                else:
                    s_dict[compound] = [].append(sorted_selectivity.get_selectivity(compound, temperature))
        for compound in s_dict:
            ax.bar(sorted_selectivity.get_temperatures(), s_dict[compound])
        return ax
