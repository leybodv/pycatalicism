import multiprocessing
import time

from pycatalicism.furnace.owen_tmp101 import OwenTPM101
from pycatalicism.mass_flow_controller.bronkhorst_f201cv import BronkhorstF201CV

class DataCollectorPlotter(multiprocessing.Process):
    """
    """

    def __init__(self, process:str, furnace_controller:OwenTPM101, mass_flow_controllers:list[BronkhorstF201CV]):
        """
        """
        super().__init__(daemon=False)
        self._furnace_controller = furnace_controller
        self._mfcs = mass_flow_controllers
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
            time.sleep(10)
        self._send_data(None, None)

    def stop(self):
        """
        """
        self._running = False

    def _collect_data(self):
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
