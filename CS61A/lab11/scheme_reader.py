"""This module implements the built-in data types of the Scheme language, along
with a parser for Scheme expressions.

In addition to the types defined in this file, some data types in Scheme are
represented by their corresponding type in Python:
    number:       int or float
    symbol:       string
    boolean:      bool
    unspecified:  None

The __repr__ method of a Scheme value will return a Python expression that
would be evaluated to the value, where possible.

The __str__ method of a Scheme value will return a Scheme expression that
would be read to the value, where possible.
"""

import numbers
import builtins

from ucb import main, trace, interact
from scheme_tokens import tokenize_lines, DELIMITERS

from buffer import Buffer, InputReader, LineReader
from pair import Pair, nil


# Scheme list parser


def scheme_read(src):
    """Read the next expression from SRC, a Buffer of tokens.

    >>> scheme_read(Buffer(tokenize_lines(['nil'])))
    nil
    >>> scheme_read(Buffer(tokenize_lines(['1'])))
    1
    >>> scheme_read(Buffer(tokenize_lines(['true'])))
    True
    >>> scheme_read(Buffer(tokenize_lines(['(+ 1 2)'])))
    Pair('+', Pair(1, Pair(2, nil)))
    """
    if src.current is None:
        raise EOFError
    val = src.pop_first()  # Get and remove the first token
    if val == 'nil':
        # BEGIN PROBLEM 2
        return nil
        # END PROBLEM 2
    elif val == '(':
        # BEGIN PROBLEM 2
        return read_tail(src)
        # END PROBLEM 2
    elif val == "'":
        # BEGIN PROBLEM 3
        "*** YOUR CODE HERE ***"

        return Pair('quote', Pair(scheme_read(src),nil))
        # END PROBLEM 3
    elif val not in DELIMITERS:
        return val
    else:
        raise SyntaxError('unexpected token: {0}'.format(val))


def read_tail(src):
    """Return the remainder of a list in SRC, starting before an element or ).

    >>> read_tail(Buffer(tokenize_lines([')'])))
    nil
    >>> read_tail(Buffer(tokenize_lines(['2 3)'])))
    Pair(2, Pair(3, nil))
    """
    try:
        while src.end_of_line():
            src.pop_first()
        if src.current is None:
            raise SyntaxError('unexpected end of file')
        elif src.current == ')':
            # BEGIN PROBLEM 2
            src.pop_first()
            return nil
            # END PROBLEM 2
        else:
            # BEGIN PROBLEM 2
            car = scheme_read(src)
            cdr = read_tail(src)
            return Pair(car, cdr)
            # END PROBLEM 2
    except EOFError:
        raise SyntaxError('unexpected end of file')


# Convenience methods


def buffer_input(prompt='scm> '):
    """Return a Buffer instance containing interactive input."""
    return Buffer(tokenize_lines(InputReader(prompt)))


def buffer_lines(lines, prompt='scm> ', show_prompt=False):
    """Return a Buffer instance iterating through LINES."""
    if show_prompt:
        input_lines = lines
    else:
        input_lines = LineReader(lines, prompt)
    return Buffer(tokenize_lines(input_lines))


def read_line(line):
    """Read a single string LINE as a Scheme expression."""
    buf = Buffer(tokenize_lines([line]))
    while buf.end_of_line():
        buf.pop_first()
    result = scheme_read(buf)
    if not buf.end_of_line():
        raise SyntaxError("read_line's argument can only be a single element, but received multiple")
    return result


# Interactive loop


def read_print_loop():
    """Run a read-print loop for Scheme expressions."""
    while True:
        try:
            src = buffer_input('read> ')
            while src.end_of_line():
                src.pop_first()
            while not src.end_of_line():
                expression = scheme_read(src)
                if expression == 'exit':
                    print()
                    return
                print('str :', expression)
                print('repr:', repr(expression))
        except (SyntaxError, ValueError) as err:
            print(type(err).__name__ + ':', err)
        except (KeyboardInterrupt, EOFError):  # <Control>-D, etc.
            print()
            return


@main
def main(*args):
    if len(args) and '--repl' in args:
        read_print_loop()


read_tail(Buffer(tokenize_lines(['2 3)'])))
