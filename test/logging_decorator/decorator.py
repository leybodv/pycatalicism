import inspect

print('Access to decorator.py')

class Decorator:

    def __init__(self, func):
        print('Decorator.__init__')
        self.func = func
        print(f'\t{self.func = }')
        print(f'\t{inspect.isfunction(self.func) = }')
        print(f'\t{inspect.ismethod(self.func) = }')
        print(f'\tMembers of self.func:')
        for member in inspect.getmembers(self.func):
            if member[0] in ['__class__', '__dict__', '__module__', '__name__', '__self__']:
                print(f'\t{member}')

    def __get__(self, obj, type=None):
        print('Decorator.__get__')
        print(f'\t{self = }')
        print(f'\t{obj = }')
        print(f'\t{type = }')
        func = self.func.__get__(obj, type)
        print(f'\t{func = }')
        print(f'\t{inspect.isfunction(func) = }')
        print(f'\t{inspect.ismethod(func) = }')
        print('\tMembers of func:')
        for member in inspect.getmembers(func):
            if member[0] in ['__class__', '__dict__', '__module__', '__name__', '__self__']:
                print(f'\t{member}')
        return self.__class__(func)

    def __call__(self, *args, **kwargs):
        print('Decorator.__call__')
        val = self.func(*args, **kwargs)
        return val
