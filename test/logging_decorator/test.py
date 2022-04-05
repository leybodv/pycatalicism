from decorator import Decorator

print('Access to test.py')

class Test:

    def __init__(self):
        print('Test.__init__')

    @Decorator
    def method(self):
        print('Test.method')
