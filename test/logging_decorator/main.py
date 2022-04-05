#!/usr/bin/python

import inspect
from decorator import Decorator
from test import Test

@Decorator
def decorated_func():
    print(' _main__.decorated_func')
    return 'return __main__.decorated_func'

if __name__ == '__main__':
    print('__main__')
    decorated_func()
    print(f'{decorated_func = }')
    print('Members of decorated_func:')
    for member in inspect.getmembers(decorated_func):
        if member[0] in ['__class__', '__dict__', '__module__', '__name__', '__self__']:
            print(f'{member}')
    t = Test()
    print(f'{t = }')
    print('Members of t:')
    for member in inspect.getmembers(t):
        if member[0] in ['__class__', '__dict__', '__module__', '__name__', '__self__']:
            print(f'{member}')
