import multiprocessing

class Plotter(multiprocessing.Process):
    """
    """

    def __init__(self):
        """
        """
        super().__init__(daemon=False)
        self._collector_pipe, self._plotter_pipe = multiprocessing.Pipe()
        self._plotter = Plotter()
        self._plotter_process = multiprocessing.Process(target=self._plotter, args=(self._plotter_pipe,), daemon=False)
        self._plotter_process.start()

    def run(self):
        """
        """
        while self._running:
            self._collect_data()
            self._send_data()
        self._send_data(None)
        raise NotImplementedError()

    def _collect_data(self):
        """
        """
        raise NotImplementedError()

    def _send_data(self):
        """
        """
        raise NotImplementedError()
