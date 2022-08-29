#!/usr/bin/python

from pathlib import Path
import random
import time

path = Path('./test.txt')

while True:
    with path.open(mode='+') as f:
        f.write(f'{random.random()}\t{random.random()}')
    time.sleep(5)
