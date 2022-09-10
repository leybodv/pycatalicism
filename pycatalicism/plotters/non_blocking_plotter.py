import multiprocessing.connection

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.axes

class NonBlockingPlotter():
    """
    Non blocking plotter that should be run in a separate process due to the incompatibility of matplotlib with multithreading. It will draw data from instance variables every minute after the process was started. Data must be sent over multiprocessing pipe.
    """

    def __init__(self):
        """
        Initialize instance variables.
        """
        self._temperatures = []
        self._flow_rates = {}

    def __call__(self, pipe:multiprocessing.connection.Connection):
        """
        Create figure and axeses, setup them, start timer and show canvas.

        parameters
        ----------
        pipe:multiprocessing.connection.Connection
            pipe through which data are get from data collector
        """
        self._pipe = pipe
        self._fig, self._left_ax = plt.subplots()
        self._setup_left_ax(self._left_ax)
        self._right_ax = self._left_ax.twinx()
        self._setup_right_ax(self._right_ax)
        timer = self._fig.canvas.new_timer(interval=60000)
        timer.add_callback(self._call_back)
        timer.start()
        plt.show()

    def _call_back(self) -> bool:
        """
        Collect data through multiprocessing pipe, append them to instance variables and add corresponding dots on plot canvas. This function is called by the matplotlib timer. Data must be sent as iterable with temperature data at 0th position and flow rates data at 1st. Temperature data is a list of floats with time at 0th position and temperature at 1st. Flow rates is a 3-element list, each containing data from different mass flow controllers. Each element is in turn a list with time at 0th position and temperature at 1st.

        returns
        -------
        timer_is_running:bool
            True if timer is needed to be run, False if it must be stopped
        """
        while self._pipe.poll():
            data = self._pipe.recv()
            temperature_point = data[0]
            flow_rate_points = data[1]
            if temperature_point is None or flow_rate_points is None:
                return False
            else:
                self._temp_time.append(temperature[0])
                self._temp_temperature.append(temperature[1])
                for i in range(3):
                    self._fr_times[i].append(flow_rates[i][0])
                    self._fr_flow_rates[i].append(flow_rates[i][1])
                self._left_ax.clear()
                self._setup_left_ax(self._left_ax)
                self._left_ax.plot(self._temp_time, self._temp_temperature)
                self._right_ax.clear()
                self._setup_right_ax(self._right_ax)
                for i in range(3):
                    self._right_ax.plot(self._fr_times[i], self._fr_flow_rates[i])
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
