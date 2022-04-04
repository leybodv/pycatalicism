#!/usr/bin/python

import inspect
import __main__ as main
from decorator import Decorator

def func():
    print('__main__.func')

if __name__ == '__main__':
    func()
    print(f'{func = }')
    print(f'{inspect.isfunction(func) = }')
    print('Members of func:')
    for member in inspect.getmembers(func):
        if member[0] in ['__class__', '__dict__', '__module__', '__name__', '__self__']:
            print(f'{member}')
    decorated_func = Decorator(func)
    decorated_func()
    print(f'{decorated_func = }')
    print(f'{inspect.isfunction(decorated_func) = }')
    print('Members of decorated_func:')
    for member in inspect.getmembers(decorated_func):
        if member[0] in ['__class__', '__dict__', '__module__', '__name__', '__self__']:
            print(f'{member}')
