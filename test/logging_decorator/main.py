#!/usr/bin/python

import inspect
import __main__ as main
from decorator import Decorator
from test import Test

def func():
    print('__main__.func')

@Decorator
def decorated_func():
    print('__main__.decorated_func')

if __name__ == '__main__':
    func()
    print(f'{func = }')
    print(f'{inspect.isfunction(func) = }')
    print(f'{inspect.ismethod(func) = }')
    print('Members of func:')
    for member in inspect.getmembers(func):
        if member[0] in ['__class__', '__dict__', '__module__', '__name__', '__self__']:
            print(f'{member}')
    reassigned_func = Decorator(func)
    reassigned_func()
    print(f'{reassigned_func = }')
    print(f'{inspect.isfunction(reassigned_func) = }')
    print(f'{inspect.ismethod(reassigned_func) = }')
    print('Members of reassigned_func:')
    for member in inspect.getmembers(reassigned_func):
        if member[0] in ['__class__', '__dict__', '__module__', '__name__', '__self__']:
            print(f'{member}')
    decorated_func()
    print(f'{decorated_func = }')
    print(f'{inspect.isfunction(decorated_func) = }')
    print(f'{inspect.ismethod(decorated_func) = }')
    print('Members of decorated_func:')
    for member in inspect.getmembers(decorated_func):
        if member[0] in ['__class__', '__dict__', '__module__', '__name__', '__self__']:
            print(f'{member}')
    t = Test()
    print(f'{t.method = }')
    print(f'{inspect.isfunction(t.method) = }')
    print(f'{inspect.ismethod(t.method) = }')
    print('Members of t.method:')
    for member in inspect.getmembers(t.method):
        if member[0] in ['__class__', '__dict__', '__module__', '__name__', '__self__']:
            print(f'{member}')

