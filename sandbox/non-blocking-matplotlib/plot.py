#!/usr/bin/python

import matplotlib.pylab as plt
import threading

def plot_fig():
    x = [1,2,3,4,5]
    y = [1,2,3,4,5]

    fig, ax = plt.subplots()
    ax.plot(x,y)
    plt.show(block=False)

print('Hello world')
thread = threading.Thread(target=plot_fig)
thread.start()
print('Goodbye world')
thread.join()
