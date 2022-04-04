import inspect

class Decorator:

    def __init__(self, func):
        print('Decorator.__init__')
        self.func = func
        print(f'{self.func = }')
        print(f'{inspect.isfunction(self.func) = }')
        print(f'Members of self.func:')
        for member in inspect.getmembers(self.func):
            if member[0] in ['__class__', '__dict__', '__module__', '__name__', '__self__']:
                print(f'{member}')

    def __call__(self, *args, **kwargs):
        print('Decorator.__call__')
        val = self.func(*args, **kwargs)
        return val
