#!/usr/bin/python

from pathlib import Path
from threading import Thread
import random
import time
import numpy as np
import matplotlib.pyplot as plt

class MyThread(Thread):
    """
    """
    def __init__(self, path):
        self.path = path
        self.fig, self.ax = plt.subplots()
        super().__init__(daemon=True)

    def run(self):
        while True:
            xs, ys = np.loadtxt(fname=self.path, delimiter='\t', unpack=True, encoding='utf-8')
            for x,y in zip(xs, ys):
                print(f'{x}\t{y}')
                self.ax.plot(x,y)
                plt.show()
            print()
            time.sleep(10)


path = Path('./test.txt')
thread = MyThread(path)
thread.start()

while True:
    with path.open(mode='a') as f:
        x = random.random()
        y = random.random()
        f.write(f'{x}\t{y}\n')
    time.sleep(5)

