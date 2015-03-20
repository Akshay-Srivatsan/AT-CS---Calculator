'''
This file contains functions relevant to user-entered special commands.
'''
from calculator import *
from expressions import *

def fix_variables(expression):
    '''
    Replaces all the variables in 'expression' with their value.
    :param expression: A string version of the expression.
    :return: The expression with all variables replaced by their value.
    '''
    for variable in memory:
        expression = expression.replace(variable, str(memory[variable]))
    return expression

def approx_derivative(expression, variable, x, h=0.0001):
    '''
    Approximates the derivative of an expression at a point.
    :param expression: The expression (as a string).
    :param variable: The independent variable.
    :param x: The point to take the derivative at.
    :param h: The accuracy (mathematically, the accuracy increases as h -> 0. In practice, small values of h introduce
        rounding errors.)
    :return: The slope of the function at that point.
    '''

    try:
        #Using %G makes python use 'E' for scientific notification, which is not ambiguous with the constant e.
        memory[variable] = '%.10f' % (x+(h/2))
        part1 = evaluate_expression(fix_variables(expression))
        memory[variable] = '%.10f' % (x-(h/2))
        part2 = evaluate_expression(fix_variables(expression))
        # raw_input()
        return (float(part1)-float(part2))/float(h)
    except TypeError as error:
        print 'Your input was invalid. The derivative of ' + expression + ' at ' + str(x) + ' could not be calculated.'
        return ''

def pick_symbol(slope):
    '''
    Picks an appropriate ASCII character based on the slope of a function. If the calculator is in simple mode, it just
        picks '*'.
    :param slope: The slope of the function.
    :return: '*' if the calculator is in simple mode, otherwise whichever one of '/', '-', '|', and '\' most closely
        matches the slope.
    '''
    if graph_mode == 'simple':
        return '*'
    # The fact that there are only five valid slopes is the reason why the inaccuracy of approx_derivative is tolerable.
    VERTICAL_THRESHOLD = 30
    HORIZONTAL_THRESHOLD = 5
    if slope >= VERTICAL_THRESHOLD:
        return '|'
    elif slope >= HORIZONTAL_THRESHOLD:
        return '/'
    elif slope > -HORIZONTAL_THRESHOLD:
        return '-'
    elif slope > -VERTICAL_THRESHOLD:
        return '\\'
    else:
        return '|'

def graph():
    '''
    Asks for an expression, x range, and output width, then graphs the expression using ASCII characters.
    This is one of the two most complicated functions in this program.
    :return: Nothing
    '''
    try:
        print '------------- Graph Generation -------------'
        print '** WARNING: Axes may not be to scale. **'
        exp = raw_input('Enter an expression, with variable \'x\': ')
        exp = exp.replace('x', '(x)')
        start = float(evaluate_expression(raw_input('Select a starting \'x\' value: ')))
        end = float(evaluate_expression(raw_input('Select an ending \'x\' value: ')))
        width = evaluate_expression(raw_input('How wide should the graph be printed?: '))-1

        print
        # The amount each x-step is equivalent to.
        step = float(end-start)/float(width)

        # Used for formatting strings for output.
        max_str_len = max(len('%0.2f' % end), len('%0.2f' % start))+3

        x_values = []
        y_values = []

        compare = lambda x, y: x <= y
        if start > end:
            compare = lambda x, y: x >= y
        i = start

        # Generate lists of all the x and y values.
        while compare(i, end):
            memory['x'] = i
            expression = exp
            expression = fix_variables(expression)
            x_values += [i]
            y_values += [float(evaluate_expression(expression))]
            i += step

        # Calculate the height of the output.
        height = len(y_values)-1

        # Calculate the difference between each y-value on the y-axis.
        ystep = (max(y_values)-min(y_values))/height

        if ystep == 0:
            # A flat line.
            ystep = 1

        # Generate x and y values relative to the output.
        mapped_x_values = map(lambda x: round(x/step, 5), x_values)
        mapped_y_values = map(lambda y: round(y/ystep, 5), y_values)

        # Offset the mapped values to make the lowest value 0.
        x_offset = min(mapped_x_values)
        mapped_x_values = map(lambda x: x - x_offset, mapped_x_values)
        y_offset = min(mapped_y_values)
        mapped_y_values = map(lambda y: y - y_offset, mapped_y_values)

        y_axis = []
        i = min(y_values)

        # I made this loop run one extra iteration, since the float rounding error sometimes cuts it off too early.
        while i - ystep <= max(y_values):
            y_axis += [i]
            i += ystep

        # Used for formatting output.
        max_y_value_len = max(len('%0.3f' % y_values[0]), len('%0.3f' % y_values[-1]))

        ran = range(int(max(mapped_y_values)), int(min(mapped_y_values)-1), -1)

        if ran == []:
            ran = [mapped_y_values[0]]

        for index in range(0, len(ran)):
            y = ran[index]
            current = ' '*int(float(end-start)/step)

            for i in range(0, len(x_values)):
                if int(mapped_y_values[i]) == int(y):
                    # For every x-value with this y-value, add the symbol with the correct slope.
                    x_val = mapped_x_values[i]
                    current = current[:int(x_val)] + pick_symbol(approx_derivative(exp, 'x', x_values[int(i)])) + current[int(x_val)+1:]
            print (('%' + str(max_y_value_len) + '.3f') % y_axis[len(ran)-index-1]) + '|' + (' '*(max_str_len-1)).join(map(lambda x: x, current))


        # This generates values for the x-axis.
        x_axis = ' '
        for x in x_values:
            x_axis += ('%' + str(max_str_len) + '.2f') % x
        print (' '*(max_y_value_len)) + ('-'*len(x_axis))
        print (' '*(max_y_value_len-3)) + x_axis

        print
        print

    except TypeError as error:
        # This will only happen if the user enters a bad expression.
        print 'Sorry, that\'s an invalid number.'

def print_table():
    '''
    Generates a table of values for an expression. A much simpler version of graph().
    :return: Nothing
    '''
    try:
        print '------------- Table Generation -------------'
        exp = raw_input('Enter an expression: ')
        variable = raw_input('Select a variable to change: ')
        start = evaluate_expression(raw_input('Select a starting ' + variable + ' value: '))
        end = evaluate_expression(raw_input('Select an ending ' + variable + ' value: '))
        step = evaluate_expression(raw_input('Select a step size: '))
        exp = exp.replace(variable, '(' + variable + ')')
        print
        print ' x          | y'
        print '------------|-------'
        i = start

        if step == 0:
            print 'Your step size is invalid.'
            return

        compare = lambda x, y: x <= y
        step = abs(step)

        if start > end:
            # Fix the step size to prevent an infinite loop.
            compare = lambda x, y: x >= y
            step = -(abs(step))

        while compare(i, end):
            memory[variable] = i
            expression = exp
            expression = fix_variables(expression)
            print i, (10 - len(str(i))) * ' ', '|', evaluate_expression(expression)
            i += step
    except ValueError as error:
        print 'Sorry, that\'s an invalid number.'

def derivative():
    '''
    A user-friendly wrapper around approx_derivative()
    :return: Nothing
    '''
    try:
        print '------------- Derivative Calculator -------------'
        print '** WARNING: This derivative is approximated using h=0.0001. **'
        exp = raw_input('Enter an expression (with variable \'x\'): ')
        x_value = evaluate_expression(raw_input('Select an \'x\' value: '))
        print approx_derivative(exp, 'x', x_value)
    except ValueError as error:
        print 'Sorry, that\'s an invalid number.'

def print_help():
    '''
    Generates a help message with a list of commands.
    :return: Nothing
    '''
    print
    print '-------------------------- Help --------------------------'
    print 'List of Commands:'
    print '\thelp\t\tShows this help message.'
    print '\ttable\t\tCreates a table of values for an expression.'
    print '\tgraph\t\tPrints a graph of a expression.'
    print '\tsimple\t\tPuts the graph into simple mode - each point is represented by a \'*\'.' + \
          (' (current mode)' if graph_mode == 'simple' else '')
    print '\tcomplex\t\tPuts the graph into complex mode - each point is represented by a symbol that best ' \
          'fits the slope of the graph at that point.' + \
          (' (current mode)' if graph_mode == 'complex' else '')
    print '\tvariables\tPrints the values of all defined variables.'
    print '\tderivative\tCalculates the derivative of a function at a point.'
    print '----------------------------------------------------------'

def print_variables():
    '''
    Prints all currently defined variables.
    :return: Nothing
    '''
    print '----------------------- Variables ------------------------'
    for variable in memory:
        print variable + '\t' + (':=' if type(memory[variable]) == str else ' =') + '\t' + repr(memory[variable])
    print '----------------------------------------------------------'


def print_welcome():
    '''
    Prints a welcome message for the user.
    :return: Nothing
    '''
    print
    print '-------------- Akshay Srivatsan\'s Calculator --------------'
    print 'Version 1.0'
    print 'Type \'help\' for a list of commands.'



def do_command(command):
    '''
    Executes a command. If the command is unrecognized, does nothing.
    :param command: The command (as a string). It must match the stored command exactly.
    :return: Nothing
    '''
    global graph_mode, memory
    # Make a copy, so any variable changes during the function are reversed at the end.
    memory_backup = dict(memory)
    if command == 'table':
        print_table()
    elif command == 'graph':
        graph()
    elif command == 'simple':
        graph_mode = 'simple'
    elif command == 'complex':
        graph_mode = 'complex'
    elif command == 'help':
        print_help()
    elif command == 'derivative':
        derivative()
    elif command == 'variables':
        print_variables()
    memory = memory_backup