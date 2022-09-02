import multiprocessing.connection

import matplotlib.pyplot as plt

class NonBlockingActivationPlotter():
    """
    """

    def __init__(self):
        """
        """
        self._temp_time = []
        self._temp_temperature = []
        self._fr_times = [[],[],[]]
        self._fr_flow_rates = [[],[],[]]

    def __call__(self, pipe:multiprocessing.connection.Connection):
        """
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
        """
        while self._pipe.poll():
            data = self._pipe.recv()
            temperature = data[0]
            flow_rates = data[1]
            if temperature is None or flow_rates is None:
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

    def _setup_left_ax(self, left_ax):
        """
        """
        left_ax.set_xlabel('Time')
        left_ax.set_ylabel('Temperature')

    def _setup_right_ax(self, right_ax):
        """
        """
        right_ax.set_ylabel('Flow rate')
