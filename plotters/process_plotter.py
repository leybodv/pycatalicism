import multiprocessing
import multiprocessing.connection
import time
import threading

from pycatalicism.furnace.owen_tmp101 import OwenTPM101
from pycatalicism.mass_flow_controller.bronkhorst_f201cv import BronkhorstF201CV
from non_blocking_plotter import NonBlockingPlotter
from pycatalicism.plotters.plotter_exceptions import PlotterException

class DataCollectorPlotter(threading.Thread):
    """
    Class for plotting data from activation and activity measurement experiments.
    """

    def __init__(self, furnace_controller:OwenTPM101, mass_flow_controllers:list[BronkhorstF201CV]):
        """
        Initialize base class, instance variables and start non blocking plotter in a separate process.

        parameters
        ----------
        furnace_controller:OwenTPM101
            furnace controller to get information about current temperature
        mass_flow_controllers:list[BronkhorstF201CV]
            list of mass flow controllers to get information about current flow rates
        """
        super().__init__(daemon=False)
        self._furnace_controller = furnace_controller
        self._mfcs = mass_flow_controllers
        self._collector_pipe, self._plotter_pipe = multiprocessing.Pipe()
        self._plotter = NonBlockingPlotter()
        self._plotter_process = multiprocessing.Process(target=self._plotter, args=(self._plotter_pipe,), daemon=False)
        self._plotter_process.start()

    def run(self):
        """
        This method is invoked when thread is started. While thread is running get temperature and flow rate data and send these data through multiprocessing pipe to non blocking plotter. Send None to plotter, when thread is not running.
        """
        self._running = True
        self._start_time = time.time()
        while self._running:
            temperature, flow_rates = self._collect_data()
            self._send_data(temperature, flow_rates)
            time.sleep(10)
        self._send_data(None, None)

    def stop(self):
        """
        Stop this thread.
        """
        self._running = False

    def _collect_data(self) -> tuple[list[float], list[list[float]]]:
        """
        Collect temperature and flow rates data and send these to plotter with time stamps.

        returns
        -------
        temperature:list[float]
            list of time (0th) and temperature(1st) collected from furnace controller
        flow_rates:list[list[float]]
            list of lists of time (0th) and flow rate (1st) data collected from all mass flow controllers
        """
        temp_t = (time.time() - self._start_time) / 60.0
        temp_T = self._furnace_controller.get_temperature()
        temperature = [temp_t, temp_T]
        flow_rates = []
        for mfc in self._mfcs:
            t = (time.time() - self._start_time) / 60.0
            fr = mfc.get_flow_rate()
            flow_rates.append([t, fr])
        return (temperature, flow_rates)

    def _send_data(self, temperature:list[float]|None, flow_rates:list[list[float]]|None):
        """
        Send data to non blocking plotter through pipe.

        parameters
        ----------
        temperature:list[float]|None
            list of time (0th) and temperature (1st) data to send to plotter or None if thread was stopped
        flow_rates:list[list[float]]|None
            list of lists of time (0th) and temperature (1st) data to send to plotter or None if thread was stopped
        """
        self._collector_pipe.send((temperature, flow_rates))
