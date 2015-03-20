'''
This is the main file: it contains all shared variables and the main loop.
'''

memory = {'E': '*10^'}
last_result = 0
graph_mode = 'complex'
list_of_commands = ['quit', 'table', 'graph', 'simple', 'complex', 'help', 'derivative', 'variables']
operators = ['+', '-', '*', '^']


# The import structure is weird because each file relies on data from every other file.
# The readline module modifies the behavior of raw_input() to provide nicer user input (arrow keys, history).
from commands import *
from expressions import *
from mixed import *
from math import *
import readline

memory['_pi'] = pi
memory['_e'] = e

def parse(expression, return_string=False):
    '''
    This function wraps evaluate_expression with some necessary prerequisites, such as checking if the input is a
    command, and substituting for variables.
    :param expression: The expression or command that the user entered at the prompt.
    :param return_string: Whether this function should return a string instead of a number.
    :return: The result of the expression, or None if the expression was invalid.
    '''

    if expression.lower() in list_of_commands:
        do_command(expression.lower())
        return None

    expression = expression.replace('_ans', (str(last_result) if last_result is not None else '0'))

    if '=' in expression and '==' not in expression:
        equal = expression.find('=')
        alias = False
        variable = expression[:equal]
        if expression[equal-1] == ':':
            alias = True
            variable = expression[:equal-1]
        variable = ''.join(filter(lambda x: x != ' ', variable))

        if variable[0] != '_':
            variable = '_' + variable
            print 'All custom variable names must begin with \'_\'. Changing to \'' + variable + '\'.'
        expression = expression[equal+1:]

        # If the user is trying to set a variable to nothing, delete the variable instead.
        if expression.replace(' ', '') == '':
            print 'Deleting variable ' + variable + '.'
            if variable not in memory:
                print 'The variable ' + variable + ' does not exist.'
                return
            del(memory[variable])
            return

        if expression == '_pi' or expression == '_e' or expression == '_E':
            print 'That variable name is reserved.'
            return

        if alias:
            result = expression
        else:
            result = parse(expression)
        memory[variable] = result
        print 'Variable \'' + variable + '\' set to \'' + str(result) + '\'.'
        return None

    expression = fix_variables(expression)

    result = evaluate_expression(expression, return_string)
    return result


if __name__ == '__main__':
    print_welcome()
    expression_or_command = ''
    while expression_or_command.lower() != 'quit' and expression_or_command.lower() != 'exit':
        try:
            print '-------------------------------'
            expression_or_command = raw_input('Enter an expression or command: ')
        except KeyboardInterrupt:
            # Control-C
            expression_or_command = 'quit'
            print
        except EOFError:
            # Control-D
            expression_or_command = 'quit'
            print
        if expression_or_command.lower() != 'quit' and expression_or_command.lower() != 'exit':
            last_result = parse(expression_or_command, True)
            if last_result is not None:
                print last_result