import multiprocessing
import multiprocessing.connection
import time
import threading

from pycatalicism.furnace.owen_tmp101 import OwenTPM101
from pycatalicism.mass_flow_controller.bronkhorst_f201cv import BronkhorstF201CV
from pycatalicism.chromatograph.chromatec_crystal_5000 import ChromatecCrystal5000
from pycatalicism.plotters.non_blocking_plotter import NonBlockingPlotter

class DataCollectorPlotter(threading.Thread):
    """
    Class for plotting data from activation and activity measurement experiments.
    """

    def __init__(self, furnace_controller:OwenTPM101, mass_flow_controllers:list[BronkhorstF201CV], chromatograph:ChromatecCrystal5000|None):
        """
        Initialize base class, instance variables and start non blocking plotter in a separate process.

        parameters
        ----------
        furnace_controller:OwenTPM101
            furnace controller to get information about current temperature
        mass_flow_controllers:list[BronkhorstF201CV]
            list of mass flow controllers to get information about current flow rates
        chromatograph:ChromatecCrystal5000
            chromatograph to get information about analysis start time
        """
        super().__init__(daemon=False)
        self._furnace_controller = furnace_controller
        self._mfcs = mass_flow_controllers
        self._chromatograph = chromatograph
        self._collector_pipe, self._plotter_pipe = multiprocessing.Pipe()
        self._plotter = NonBlockingPlotter()
        self._plotter_process = multiprocessing.Process(target=self._plotter, args=(self._plotter_pipe,), daemon=False)
        self._plotter_process.start()

    def run(self):
        """
        This method is invoked when thread is started. While thread is running get temperature, chromatograph and flow rate data and send these data through multiprocessing pipe to non blocking plotter. Send None to plotter, when thread is not running.
        """
        self._running = True
        self._start_time = time.time()
        while self._running:
            temperature_point, chromatograph_point, flow_rate_points = self._collect_data()
            self._collector_pipe.send((temperature_point, chromatograph_point, flow_rate_points))
            time.sleep(10)
        self._collector_pipe.send((None, None, None))

    def stop(self):
        """
        Stop this thread.
        """
        self._running = False

    def _collect_data(self) -> tuple[Point, Point, list[Point]]:
        """
        """
        t = (time.time() - self._start_time) / 60.0
        T = self._furnace_controller.get_temperature()
        temperature_point = Point(x=t, y=T, label='temperature')
        chromatograph_point = None
        if self._chromatograph is not None:
            if self._chromatograph.get_status() is WorkingStatus.ANALYSIS:
                t = round((time.time() - self._start_time) / 60.0, 2) - self._chromatograph.get_analysis_time()
                chromatograph_point = Point(x=t, y=None, label='chromatograms')
        flow_rate_points = []
        for mfc, gas in zip(self._mfcs, self._gases):
            t = (time.time() - self._start_time) / 60.0
            fr = mfc.get_flow_rate()
            flow_rate_point = Point(x=t, y=fr, label=gas)
            flow_rate_points.append(flow_rate_point)
        return (temperature_point, chromatograph_point, flow_rate_points)
