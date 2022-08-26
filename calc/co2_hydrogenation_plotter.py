from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.axes
import numpy as np

from calc.plotter import Plotter
from calc.plotterexception import PlotterException
from calc.conversion import Conversion
from calc.selectivity import Selectivity
from logging_decorator import Logging

class CO2HydrogenationPlotter(Plotter):
    """
    Class for plotting CO2 hydrogenation conversion and selectivity data and exporting resulting plots to file.
    """

    @Logging
    def __init__(self):
        """
        Registers logger with instances of this class which can be accessed via self.logger instance variable
        """
        super().__init__()

    def plot(self, conversion:Conversion|None, selectivity:Selectivity|None, show_plot:bool=False, output_plot_path:Path|None=None, plot_title:str|None=None):
        """
        Main interface of this class. Plots conversion vs. temperature as line plot and selectivities vs. temperature as bar plot. If show_plot is true, shows plots. If output_data_path was provided, exports plots to result.png to provided directory

        parameters
        ----------
        conversion:Conversion
            wrapper for CO2 conversion at different temperatures data
        selectivity:Selectivity
            wrapper for selectivities to different compounds at different temperatures data
        show_plot:bool (default:False)
            if True, show plots
        output_data_path:Path|None (default:None)
            path to directory to export data

        raises
        ------
        PlotterException
            if conversion and selectivities are None
        """
        if conversion and selectivity:
            fig, (ax_conversion, ax_selectivity) = plt.subplots(nrows=1, ncols=2)
            ax_conversion = self._plot_conversion(ax_conversion, conversion)
            ax_selectivity = self._plot_selectivity(ax_selectivity, selectivity)
        elif conversion and not selectivity:
            fig, ax_conversion = plt.subplots()
            ax_conversion = self._plot_conversion(ax_conversion, conversion)
        elif selectivity and not conversion:
            fig, ax_selectivity = plt.subplots()
            ax_selectivity = self._plot_selectivity(ax_selectivity, selectivity)
        else:
            raise PlotterException('Nothing to plot')
        if plot_title:
            fig.suptitle(plot_title)
        if show_plot:
            self.logger.info(f'Plotting conversion vs. temperature for CO2 hydrogenation reaction')
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
        Plot CO2 conversion vs. temperature plot as line plot.

        parameters
        ----------
        ax:Axes
            axes to plot to
        conversion:Conversion
            wrapper to CO2 conversion at different temperatures data

        returns
        -------
        ax:Axes
            axes with plotted data
        """
        sorted_conversion = conversion.get_sorted()
        ax.plot(sorted_conversion.get_temperatures(), sorted_conversion.get_alphas(), marker='o', markersize=5)
        _max = sorted_conversion.get_alphas().max()
        _min = sorted_conversion.get_alphas().min()
        delta = _max - _min
        ax.set_ylim(bottom=_min - 0.1 * delta, top=_max + 0.1 * delta)
        ax.set_xlabel('Temperature, °C')
        ax.set_ylabel('$\mathrm{CO_2}$ conversion')
        return ax

    def _plot_selectivity(self, ax:matplotlib.axes.Axes, selectivity:Selectivity) -> matplotlib.axes.Axes:
        """
        Plot selectivities to different compounds at different temperatures as bar plot

        parameters
        ----------
        ax:Axes
            axes to plot to
        selectivity:Selectivity
            wrapper with selectivity data

        returns
        -------
        ax:Axes
            axes with plotted data
        """
        sorted_selectivity = selectivity.get_sorted()
        self.logger.debug(f'{str(sorted_selectivity) = }')
        s_dict = {}
        for temperature in sorted_selectivity.get_temperatures():
            self.logger.debug(f'{temperature = }')
            for compound in sorted_selectivity.get_selectivities_at(temperature):
                self.logger.debug(f'{compound = }')
                self.logger.debug(f'{s_dict = }')
                if compound in s_dict:
                    self.logger.debug(f'{sorted_selectivity.get_selectivity(compound, temperature) = }')
                    s_dict[compound].append(sorted_selectivity.get_selectivity(compound, temperature))
                else:
                    self.logger.debug(f'{sorted_selectivity.get_selectivity(compound, temperature) = }')
                    s_dict[compound] = [sorted_selectivity.get_selectivity(compound, temperature)]
        compounds = list(s_dict)
        bottom = 0
        for i in range(len(compounds)):
            self.logger.debug(f'{compounds[i] = }')
            self.logger.debug(f'{sorted_selectivity.get_temperatures() = }')
            self.logger.debug(f'{s_dict[compounds[i]] = }')
            self.logger.debug(f'{bottom = }')
            if not np.all(np.array(s_dict[compounds[i]]) == 0):
                ax.bar(sorted_selectivity.get_temperatures(), s_dict[compounds[i]], bottom=bottom, width=5, label=compounds[i])
                bottom = bottom + np.array(s_dict[compounds[i]])
        ax.set_xlabel('Temperature, °C')
        ax.set_ylabel('Selectivity')
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        return ax
