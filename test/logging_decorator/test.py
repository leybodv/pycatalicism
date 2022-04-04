from decorator import Decorator

class Test:

    def __init__(self):
        print('Test.__init__')

    @Decorator
    def method(self):
        print('Test.method')
