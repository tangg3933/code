class ExampleClass(object):
    def __init__(self, number):
        self.number = number
        
    def get_object(self):
        return ExampleClass(self.number + 1)
        
def get_string(str):
    return 'Hello ' + str
