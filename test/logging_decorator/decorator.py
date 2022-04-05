import inspect

print('\tAccess to decorator.py')

class Decorator:

    def __init__(self, decor_func):
        print('\tDecorator.__init__')
        print(f'\t{self = }')
        print(f'\tMembers of self:')
        for member in inspect.getmembers(self):
            if member[0] in ['__class__', '__dict__', '__module__', '__name__', '__self__']:
                print(f'\t{member}')
        print(f'\t{decor_func = }')
        print(f'\tMembers of decor_func:')
        for member in inspect.getmembers(decor_func):
            if member[0] in ['__class__', '__dict__', '__module__', '__name__', '__self__']:
                print(f'\t{member}')
        self.func = decor_func

    def __get__(self, obj, type=None):
        print('Decorator.__get__')
        print(f'\t{self = }')
        print(f'\t{obj = }')
        print(f'\t{type = }')
        new_func = self.func.__get__(obj, type)
        print(f'\t{new_func = }')
        print('\tMembers of new_func:')
        for member in inspect.getmembers(new_func):
            if member[0] in ['__class__', '__dict__', '__module__', '__name__', '__self__']:
                print(f'\t{member}')
        return self.__class__(new_func)

    def __call__(self, *args, **kwargs):
        print('\tDecorator.__call__')
        print(f'\t{args = }')
        print(f'\t{kwargs = }')
        val = self.func(*args, **kwargs)
        print(f'\t{val = }')
        return val
