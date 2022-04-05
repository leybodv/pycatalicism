from decorator import Decorator
import inspect

print('\t\tAccess to test.py')

class Test:

    @Decorator
    def __init__(self):
        print('\t\tTest.__init__')
        print(f'\t\t{self = }')
        print('\t\tMembers of self:')
        for member in inspect.getmembers(self):
            if member[0] in ['__class__', '__dict__', '__module__', '__name__', '__self__']:
                print(f'\t\t{member}')
