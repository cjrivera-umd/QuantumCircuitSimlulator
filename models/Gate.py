from math import log2

class Gate():

    def __init__(self, matrix, name, alias=None):
        self.matrix = matrix
        self.name = name
        self.alias = alias

        self.input_size = int(log2(len(self.matrix.matrix)))


    def getListName(self):
        return f'{self.name} {f"({self.alias})" if self.alias else ""}'


    def getButtonName(self):
        return self.alias if self.alias else self.name
    

    def __eq__(self, other):
        return self.name == other.name
    
    
    def __repr__(self):
        return f'{self.getListName()}'