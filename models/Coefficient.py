
class Coefficient():

    def __init__(self, num, den=1, num_sqrt=False, den_sqrt=False):
        self.num = num
        self.den = den
        self.num_sqrt = num_sqrt
        self.den_sqrt = den_sqrt


    def modulus_squared(self):
        new_den = self.den if self.den_sqrt else self.den ** 2
        new_num = self.num if self.num_sqrt else self.num ** 2

        print(f'{new_num}/{new_den}')
        return new_num / new_den


    def __mul__(self, other):
        # Denominator math
        if self.den_sqrt and other.den_sqrt: # Both are squared
            new_den = self.den if self.den == other.den else self.den * other.den
            new_den_sqrt = self.den != other.den
        elif self.den_sqrt:
            new_den = self.den * (other.den ** 2)
            new_den_sqrt = True
        elif other.den_sqrt:
            new_den = (self.den ** 2) * other.den
            new_den_sqrt = True
        else: # Neither is squared
            new_den = self.den * other.den
            new_den_sqrt = False

        # Numerator math
        if self.num_sqrt and other.num_sqrt: # Both are squared
            new_num = self.num if self.num == other.num else self.num * other.num
            new_num_sqrt = self.num != other.num
        elif self.num_sqrt:
            new_num = self.num * (other.num ** 2)
            new_num_sqrt = True
        elif other.num_sqrt:
            new_num = (self.num ** 2) * other.num
            new_num_sqrt = True
        else: # Neither is squared
            new_num = self.num * other.num
            new_num_sqrt = False

        return Coefficient(new_num, new_den, new_num_sqrt, new_den_sqrt)


    def __repr__(self):
        return f'{"√" if self.num_sqrt else ""}{self.num}/{"√" if self.den_sqrt else ""}{self.den}'