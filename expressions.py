'''
This file contains functions relevant to parsing expressions.
'''
from calculator import *
from commands import *
from fraction import *
from mixed import *
from math import *

def evaluate_expression(expression, return_string=False):
    '''
    This function catches any errors that might occur when generating or evaluating the tree.
    :param expression: A string form of the expression.
    :param return_string: Whether to return a string instead of a number.
    :return: The result, or None if there is an error.
    '''
    tree = to_tree(expression)
    try:
        return evaluate_tree(tree, return_string=return_string)

    except ValueError as error:
        if 'negative number cannot be raised to a fractional power' in str(error):
            print 'Error: you can\'t take the root of a negative number.'
        else:
            print 'Error: input out of domain.'
    except ZeroDivisionError as error:
        if 'fraction' in str(error):
            print 'Error: you can\'t have a fraction with a denominator of zero.'
        else:
            print 'Error: you can\'t divide by zero.'
    except NameError as error:
        if 'is not defined' in str(error):
            # Find the name of the variable that isn't defined, then find the location in the string.
            space1 = str(error).find(' ')
            space2 = space1 + str(error)[space1+1:].find(' ')
            variable = str(error)[space1+2:space2]
            if variable.endswith('fraction'):
                # The user attempted to define an invalid mixed number, which confused the parser.
                print 'Your input doesn\'t make sense. Make sure that all fractions and mixed numbers are properly ' \
                      'parenthesized.'
                return
            print 'The variable \'' + variable + '\' is not defined.'
            print '\t' + expression
            print '\t' + expression.find(variable)*' ' + '^'
        else:
            print str(error)
    except SyntaxError as error:
        # Point to the end of the expression, since this exception is almost always the result of an incomplete input.
        print 'Your expression seems to be incomplete. Are you sure you didn\'t mean to put something here?'
        print '\t' + expression
        print '\t' + ' '*len(expression) + '^'
    except TypeError as error:
        print 'Your input doesn\'t make sense. Are you sure you didn\'t make a typo?'


# A simple check to see if an object is not a list.
is_atom = lambda x: type(x) != list


def is_flat(tree):
    '''
    Tests to see if the tree is a flat list.
    :param tree: The tree to test.
    :return: True if the tree is flat, False if it contains nested lists.
    '''
    return reduce(lambda old, current: is_atom(current) and old, tree, True)


def filter_tree(predicate, tree):
    '''
    A version of filter that works on trees.
    :param predicate: A function that returns True if the element should be included.
    :param tree: The tree to evaluate.
    :return: A version of the tree containing only the elements for which predicate returned True
    '''
    if is_atom(tree):
        return tree if (predicate(tree)) else None
    else:
        newTree = []
        for i in tree:
            tmp = filter_tree(predicate, i)
            newTree += [tmp] if tmp is not None else []
        return newTree


def map_tree(transformation, tree):
    '''
    A version of map that works on trees.
    :param transformation: A function that changes a value of an element.
    :param tree: The tree to evaluate.
    :return: A version of the tree which every element has been replaced by transformation(element).
    '''
    if is_atom(tree):
        return transformation(tree)
    else:
        return map(lambda x: map_tree(transformation, x), tree)


def process_exceptions(string):
    '''
    Processes mixed numbers and fractions, which need to be changed from user-readable form to eval-readable form.
    :param string: The string representing one number.
    :return: A version of the number that eval can interpret.
    '''
    if string == None:
        return ''
    if string[-1] == '/' and len(string) > 1:
        return 'float(' + string[:-1] + ')/'
    elif ' ' in string and '/' in string:
        space = string.find(' ')
        bar = string.find('/')
        return 'mixed(' + string[space + 1:bar] + ',' + string[bar + 1:] + ',' + string[:space] + ')'
    elif '/' in string and '.' not in string and len(string) > 1:
        bar = string.find('/')
        rest = string[bar + 1:]
        if '/' in rest:
            # A fraction in another fraction.
            end = reduce(lambda x, y: y if y < x and y != -1 else x, [len(rest)-1, rest.find(')')])
            return 'fraction(' + string[:bar] + ',' + rest[:end-1] + ')' + rest[end-1:]
        else:
            return 'fraction(' + string[:bar] + ',' + string[bar+1:] + ')'
    else:
        return string


def evaluate_tree(tree, depth=0, return_string=False):
    '''
    Evaluates a tree built of operators and operands.
    :param tree: The tree to evaluate.
    :param depth: The depth of recursion.
    :param return_string: Whether to return a string or a number.
    :return: A number which is the answer, or a string which represents the number, depending on the value of
        return_string.
    '''
    if is_atom(tree):
        return process_exceptions(tree)
    else:
        if len(tree) == 0:
            return None
        if is_flat(tree) and ('/' in tree):
            # This makes sure that there wasn't a fraction that was ignored because of stray parentheses.
            return repr(evaluate_expression(''.join(tree)))
        tmp = str(reduce(lambda x, y: x + y, map(lambda x: evaluate_tree(x, depth + 1, return_string), tree)))

        if (depth > 0):
            retval = repr(eval(tmp))
            if retval[0] != '(' or retval[-1] != ')':
                # The only place where this would not run is in the input to a function.
                retval = '(' + retval + ')'
            return retval
        else:
            if (tmp != ''):
                retval = eval(tmp)
                if not return_string or type(retval) != float:
                    return retval
                else:
                    return ('%G' % retval)
            else:
                return 0



def to_tree(expression):
    '''
    Converts an expression string into a tree. This is one of the two most complicated functions in this program.
    It recursively traverses the tree, converting parentheses into nested lists.
    :param expression: The string version of the expression.
    :return: The tree version of the expression.
    '''
    tree = ['']
    index = 0
    depth = 0
    previous_toplevel_parenthesis = -1

    # Go through the tree, converting tokens into tree elements and calling to_tree on expressions within parentheses.
    while (index != len(expression)):
        if expression[index] == '(':
            if depth == 0:
                previous_toplevel_parenthesis = index
            depth += 1
        elif expression[index] == ')':
            depth -= 1
            if depth == 0:
                tree += [to_tree(expression[previous_toplevel_parenthesis + 1:index])]
        else:
            if depth == 0:
                cur = expression[index]
                if cur in operators:
                    tree += [expression[index], '']
                else:
                    tree[-1] += cur
        index += 1

    if depth != 0:
        return None

    # These get rid of all spaces except for in mixed numbers.
    tmp = filter_tree(lambda x: x != ' ' and x != '', tree)
    tmp = map_tree(lambda x: x if x[-1] != ' ' else x[:-1], tmp)
    tmp = map_tree(lambda x: x if x[0] != ' ' else x[1:], tmp)

    # This substitutes '**' for '^'.
    tmp = map_tree(lambda x: x if x != '^' else '**', tmp)
    return tmp
