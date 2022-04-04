import inspect

class Decorator:

    def __init__(self, func):
        print('Decorator.__init__')
        self.func = func
        print(f'{self.func = }')
        print(f'{inspect.isfunction(self.func) = }')
        print(f'{inspect.ismethod(self.func) = }')
        print(f'Members of self.func:')
        for member in inspect.getmembers(self.func):
            if member[0] in ['__class__', '__dict__', '__module__', '__name__', '__self__']:
                print(f'{member}')

    def __get__(self, obj, type=None):
        print('Decorator.__get__')
        func = self.func.__get__(obj, type)
        print(f'{func = }')
        print(f'{inspect.isfunction(func) = }')
        print(f'{inspect.ismethod(func) = }')
        print('Members of func:')
        for member in inspect.getmembers(func):
            if member[0] in ['__class__', '__dict__', '__module__', '__name__', '__self__']:
                print(f'{member}')
        return self.__class__(func)

    def __call__(self, *args, **kwargs):
        print('Decorator.__call__')
        val = self.func(*args, **kwargs)
        return val
