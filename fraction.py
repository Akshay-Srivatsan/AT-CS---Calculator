def gcd(a,b):
    '''
    Calculates the GCD of two numbers.
    :param a: The first number
    :param b: The second number
    :return: The greatest common divisor of the two numbers.
    '''
    while b != 0:
        t = b
        b = a % b
        a = t
    return a


class fraction (object):
    '''
    A fraction represents a ratio between two integers. This class provides standard operations for fractions, as well
    as "reverse" operations, which are used to operate on a fraction and another type of number.
    '''
    def __init__ (self, numerator=0, denominator=1):
        '''
        Tests if the denominator is zero, then simplifies the fraction. Also takes care of floats in the numerator or
            denominator.
        :param numerator: The numerator.
        :param denominator: The denominator.
        :return: Nothing
        '''
        numerator = float(numerator)
        denominator = float(denominator)
        if denominator == 0:
            raise ZeroDivisionError, 'fraction with zero denominator'
        if (int(numerator) != numerator or int(denominator) != denominator):
            numerator *= 10
            denominator *= 10
        self.numerator = int(numerator / gcd(numerator, denominator))
        self.denominator = int(denominator / gcd(numerator, denominator))

    def get_numerator(self):
        return self.numerator

    def get_denominator(self):
        return self.denominator

    def __str__(self, simplify = False):
        '''
        Generates a string version of the fraction in the format (X/Y). If the denominator is 1 and simplify is set,
            prints only the numerator.
        :return: The string version.
        '''
        if self.denominator != 1 or not simplify:
            return '(' + str(self.numerator) + '/' + str(self.denominator) + ')'
        else:
            return str(self.numerator)

    def __repr__(self):
        '''
        Generates a string version of the fraction in eval-readable form.
        :return: The string.
        '''
        return 'fraction(' + str(self.numerator) + ', ' + str(self.denominator) + ')'

    def __add__(self, other):
        if type(self) == type(other):
            return self.__class__(self.numerator * other.denominator + self.denominator * other.numerator, self.denominator * other.denominator)
        else:
            return self.__radd__(other)

    def __radd__(self, other):
        return self.__class__(float(other) + float(self), 1)

    def __sub__(self, other):
        if type(self) == type(other):
            return self + fraction(other.numerator * -1, other.denominator)
        else:
            return -(self.__rsub__(other))

    def __rsub__(self, other):
        return self.__class__(float(other) - float(self), 1)

    def __mul__(self, other):
        if type(self) == type(other):
            return self.__class__(self.numerator * other.numerator, self.denominator * other.denominator)
        else:
            return self.__rmul__(other)

    def __rmul__(self, other):
        return self.__class__(float(other) * float(self), 1)

    def __div__(self, other):
        if type(self) == type(other):
            return self * other.reciprocal()
        else:
            return self.__rdiv__(other).reciprocal()

    def __rdiv__(self, other):
        return self.__class__(float(other) / float(self), 1)

    def __float__(self):
        return float(self.numerator)/self.denominator

    def __pow__(self, other):
        return self.__class__(self.numerator**float(other), self.denominator**float(other))

    def __rpow__(self, other):
        return self.__class__(float(other) ** float(self), 1)

    def __neg__(self):
        return self.__class__(-1*self.numerator, self.denominator)

    def __lt__(self, other):
        return float(self) < float(other)

    def __le__(self, other):
        return float(self) <= float(other)

    def __gt__(self, other):
        return float(self) > float(other)

    def __ge__(self, other):
        return float(self) >= float(other)

    def __ne__(self, other):
        return float(self) != float(other)

    def __abs__(self):
        return self.__class__(abs(self.numerator), abs(self.denominator))

    def reciprocal(self):
        return self.__class__(self.denominator, self.numerator)

