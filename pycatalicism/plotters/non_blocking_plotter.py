import multiprocessing.connection

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.axes

from pycatalicism.plotters.data import Data

class NonBlockingPlotter():
    """
    Non blocking plotter that should be run in a separate process due to the incompatibility of matplotlib with multithreading. It will draw data from instance variables every minute after the process was started. Data must be sent over multiprocessing pipe.
    """

    def __init__(self):
        """
        Initialize instance variables.
        """
        self._temperatures = Data(label='temperature')
        self._chromatograms = None
        self._flow_rates = None

    def __call__(self, pipe:multiprocessing.connection.Connection):
        """
        Create figure and axeses, setup them, start timer and show canvas.

        parameters
        ----------
        pipe:multiprocessing.connection.Connection
            pipe through which data are get from data collector
        """
        self._pipe = pipe
        self._fig = plt.figure()
        self._left_ax = self._fig.add_axes([0.1, 0.1, 0.6, 0.85]) # left, bottom, right, top
        self._setup_left_ax(self._left_ax)
        self._right_ax = self._left_ax.twinx()
        self._setup_right_ax(self._right_ax)
        timer = self._fig.canvas.new_timer(interval=60000)
        timer.add_callback(self._call_back)
        timer.start()
        plt.show()

    def _call_back(self) -> bool:
        """
        Collect data through multiprocessing pipe, append them to instance variables and add corresponding dots on plot canvas. This function is called by the matplotlib timer. Data must be sent in a 3-element tuple: (temperature_point, chromatogram_point, list-of-flow-rate-points). Each data point is wrapped as Point object.

        returns
        -------
        timer_is_running:bool
            True if timer is needed to be run, False if it must be stopped
        """
        while self._pipe.poll():
            data = self._pipe.recv()
            temperature_point = data[0]
            chromatogram_point = data[1]
            flow_rate_points = data[2]
            if temperature_point is None:
                return False
            else:
                self._temperatures.add_point(temperature_point)
                if chromatogram_point is not None:
                    if self._chromatograms is None:
                        self._chromatograms = Data(label='chromatograms')
                    self._chromatograms.add_point(chromatogram_point)
                if self._flow_rates is None:
                    self._flow_rates = []
                    for flow_rate_point in flow_rate_points:
                        self._flow_rates.append(Data(label=flow_rate_point.get_label()))
                for flow_rate_point, flow_rate in zip(flow_rate_points, self._flow_rates):
                    flow_rate.add_point(flow_rate_point)
                self._left_ax.clear()
                self._right_ax.clear()
                self._setup_left_ax(self._left_ax)
                self._setup_right_ax(self._right_ax)
                lines = []
                line, = self._left_ax.plot(self._temperatures.get_x(), self._temperatures.get_y(), color='red', linewidth=1, linestyle=':', label=self._temperatures.get_label())
                lines.append(line)
                if self._chromatograms is not None:
                    line = self._left_ax.vlines(self._chromatograms.get_x(), self._left_ax.get_ylim()[0], self._left_ax.get_ylim()[1], colors=['#000000'], linewidth=1, label=self._chromatograms.get_label())
                    lines.append(line)
                for flow_rate in self._flow_rates:
                    line, = self._right_ax.plot(flow_rate.get_x(), flow_rate.get_y(), linewidth=1, linestyle=':', label=flow_rate.get_label())
                    lines.append(line)
                self._left_ax.legend(handles=lines, bbox_to_anchor=(1.1, 1), loc='upper left', borderaxespad=0)
        self._fig.canvas.draw()
        return True

    def _setup_left_ax(self, left_ax:matplotlib.axes.Axes):
        """
        Setup left, temperature, axes. Set x and y labels

        parameters
        ----------
        left_ax:matplotlib.axes.Axes
            axes to setup
        """
        left_ax.set_xlabel('Time, min')
        left_ax.set_ylabel('Temperature, °C')

    def _setup_right_ax(self, right_ax:matplotlib.axes.Axes):
        """
        Setup right, flow rates, axes. Sets y label.

        parameters
        ----------
        right_ax:matplotlib.axes.Axes
            axes to setup
        """
        right_ax.set_ylabel('Flow rate, n.ml/min')
