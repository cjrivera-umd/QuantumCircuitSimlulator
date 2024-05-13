import numpy as np

from models.Coefficient import Coefficient

class Matrix():

    def __init__(self, array, coef=Coefficient(1), shape=None):
        self.coef = coef
        self.matrix = np.array(array)
        if shape:
            self.matrix.shape = shape


    # Overloading the * operator for matrix multiplication
    def __mul__(self, other):
        new_coef = self.coef * other.coef
        new_matrix = np.matmul(self.matrix, other.matrix)
        
        # Simplifying the matrix
        shape, flattened = new_matrix.shape, new_matrix.flatten()
        non_one_coef = list(filter(lambda elem: elem != 0 and elem != 1, flattened))

        if not non_one_coef:
            return Matrix(new_matrix, new_coef)

        non_one_coef = non_one_coef[0]
        if all((not elem or elem / non_one_coef == 1) for elem in flattened):
            new_matrix = (flattened / non_one_coef).astype(int)
            new_matrix.shape = shape
            new_coef = new_coef * Coefficient(non_one_coef)

        return Matrix(new_matrix, new_coef)
    

    # Overloading the ** operator for tensor product
    def __pow__(self, other):
        new_coef = self.coef * other.coef
        return Matrix(np.kron(self.matrix, other.matrix), new_coef)
    

    def T(self):
        print(self)
        return Matrix(np.transpose(self.matrix))
    

    def norm(self):
        _, cols = self.matrix.shape
        if cols != 1:
            print('Not a state vector')
            return

        if not len(np.where(self.matrix != [0])[0]):
            return 0
        
        return self.coef.modulus_squared()
    

    def toBitstring(self, length):
        _, cols = self.matrix.shape
        if cols != 1 or not len(np.where(self.matrix != [0])[0]):
            print('Not a state vector')
            return
        
        position = np.where(self.matrix != [0])[0][0]
        return format(position, f'0{length}b')
    

    def __len__(self):
        return len(self.matrix)
    

    def __repr__(self):
        return f'{self.coef}\t' + '\n\t'.join([str(row) for row in self.matrix])