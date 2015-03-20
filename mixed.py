from fraction import *

class mixed(fraction):
    '''
    A mixed number is a wrapper around a fraction that prints it out in a easier-to-read format.
    Most functionality is inherited from fraction.
    '''

    def __init__(self, numerator=0, denominator=1, whole=0):
        '''
        Stores all data as an improper fraction.
        :param numerator: The numerator of the fraction.
        :param denominator: The denominator of the fraction.
        :param whole: The whole number component of the mixed number.
        :return: Nothing
        '''
        if whole < 0:
            # Make sure the whole part and numerator have the correct signs relative to each other.
            numerator *= -1
        super(mixed, self).__init__(whole*denominator + numerator, denominator)

    def __str__(self, simplify=True, absolute=False):
        '''
        Generates a string version of the mixed number, in the form (W X/Y)
        :param simplify: Whether to eliminate missing terms (e.g., if the whole number is 0, don't print it).
        :return: The string version of the mixed number.
        '''
        negative = False
        numerator = super(mixed, self).get_numerator()
        negative |= numerator > 0
        denominator = super(mixed, self).get_denominator()
        negative ^= denominator > 0
        whole = abs(numerator)/abs(denominator) * (-1 if negative and not absolute else 1)
        numerator = abs(numerator) % abs(denominator)
        retval = '('
        if whole != 0 or not(simplify):
            retval += str(whole)
        if (whole != 0 and numerator != 0) or not(simplify):
            retval += ' '
        if numerator != 0 or not(simplify):
            retval += str(fraction(numerator, denominator))[1:-1]
        return retval + ')'

    def __repr__(self):
        '''
        Creates a string version of the mixed number in the format that eval can use.
        :return: A string in the python interpreter format.
        '''
        s = self.__str__(False)
        whole = s[1:s.find(' ')]
        numerator = s[s.find(' ')+1: s.find('/')]
        denominator = s[s.find('/')+1:-1]
        return 'mixed(whole=' + str(whole) + ', numerator=' + str(numerator) + ', denominator=' + str(denominator) + ')'

