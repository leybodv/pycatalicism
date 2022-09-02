import multiprocessing
import multiprocessing.connection
import time

from pycatalicism.furnace.owen_tmp101 import OwenTPM101
from pycatalicism.mass_flow_controller.bronkhorst_f201cv import BronkhorstF201CV
from pycatalicism.plotters.non_blocking_activation_plotter import NonBlockingActivationPlotter
from pycatalicism.plotters.non_blocking_measurement_plotter import NonBlockingMeasurementPlotter
from pycatalicism.plotters.plotter_exceptions import PlotterException

class DataCollectorPlotter(multiprocessing.Process):
    """
    """

    def __init__(self, process:str, furnace_controller:OwenTPM101, mass_flow_controllers:list[BronkhorstF201CV], stopper_pipe:multiprocessing.connection.Connection):
        """
        """
        super().__init__(daemon=False)
        self._furnace_controller = furnace_controller
        self._mfcs = mass_flow_controllers
        self._stopper_pipe = stopper_pipe
        self._collector_pipe, self._plotter_pipe = multiprocessing.Pipe()
        if process == 'activation':
            self._plotter = NonBlockingActivationPlotter()
        elif process == 'measurement':
            self._plotter = NonBlockingMeasurementPlotter()
        else:
            raise PlotterException(f'Unknown process {process}')
        self._plotter_process = multiprocessing.Process(target=self._plotter, args=(self._plotter_pipe,), daemon=False)
        self._plotter_process.start()

    def run(self):
        """
        """
        self._running = True
        self._start_time = time.time()
        while self._running:
            temperature, flow_rates = self._collect_data()
            self._send_data(temperature, flow_rates)
            if self._stopper_pipe.poll():
                self._running = self._stopper_pipe.recv()
            time.sleep(10)
        self._send_data(None, None)

    def _collect_data(self) -> tuple[list[float], list[list[float]]]:
        """
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
        """
        self._collector_pipe.send((temperature, flow_rates))
