from enum import Enum

from models.Matrix import Matrix
from models.Coefficient import Coefficient

class InitialState(Enum):
    ZERO = {
        'repr': '0',
        'vector': Matrix([[1], [0]])
    }
    ONE = {
        'repr': '1',
        'vector': Matrix([[0], [1]])
    }
    PLUS = {
        'repr': '+',
        'vector': Matrix([[1], [1]], Coefficient(1, 2, den_sqrt=True))
    }
    MINUS = {
        'repr': '–',
        'vector': Matrix([[1], [-1]], Coefficient(1, 2, den_sqrt=True))
    }