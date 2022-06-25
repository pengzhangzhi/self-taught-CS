import sys

from libfuturize.fixes.fix_cmp import expression

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms


##############
# Eval/Apply #
##############


def scheme_eval(expr, env, _=None):  # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 3
        procedure = scheme_eval(first, env)
        validate_procedure(procedure)
        from functools import partial
        args = rest.map(lambda x: scheme_eval(x, env))
        # print("procedure: ",procedure)
        # print("args: ",args)
        return scheme_apply(procedure, args, env)
        # evaluate the operator to a Procedure instance
        # return scheme_apply(procedure, args, env)
        # END PROBLEM 3


def convert_pair_to_list(pair):
    """ convert a pair obj to a list.
        Args:
            Pair: a pair obj
        Returns:
            a list where each element is a element from pair with the same order.
        >>> pair = Pair(1,Pair(2,Pair(3,Pair(Pair(4,Pair(5,Pair(6,Pair(7,nil)))),nil))))
        >>> convert_pair_to_list(pair)
        >>> [1, 2, 3, 4, 5, 6, 7]
    """
    if pair is nil:
        return []
    # if isinstance(pair.first, Pair):
    #     first = convert_pair_to_list(pair.first)
    else:
        first = [pair.first]
    if pair.rest is nil:
        rest = []
    elif isinstance(pair.rest, Pair):
        rest = convert_pair_to_list(pair.rest)
    else:
        rest = [pair.rest]
    return first + rest


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    validate_procedure(procedure)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        "*** YOUR CODE HERE ***"
        try:
            # convert Pair obj into list
            # if require env, append env to the list
            # call the procedure and return the result
            arg_list = convert_pair_to_list(args)
            if procedure.expect_env:
                arg_list.append(env)
            return procedure.py_func(*arg_list)
        except TypeError:
            raise SchemeError(f'incorrect number of arguments of'
                              f' {len(arg_list)},\n {arg_list}, \n {args}\n'
                              f'for procedure {procedure.py_func}')
        # END PROBLEM 2
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        frame = env.make_child_frame(procedure.formals,args)
        body = procedure.body
        return eval_all(body,frame)
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        frame = env.make_child_frame(procedure.formals, args)
        body = procedure.body
        return eval_all(body, frame)
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)


def eval_all(expressions, env):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 6
    # print("expression:", expressions)
    # print("type:", type(expressions))
    if expressions is nil:
        return None
    first = scheme_eval(expressions.first, env)
    if expressions.rest is nil:
        return first
    else:
        # print(env.bindings.keys())
        return eval_all(expressions.rest, Frame(env))

    # END PROBLEM 6


##################
# Tail Recursion #
##################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val


def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""

    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN PROBLEM EC
        "*** YOUR CODE HERE ***"
        # END PROBLEM EC

    return optimized_eval

################################################################
# Uncomment the following line to apply tail call optimization #
################################################################
# scheme_eval = optimize_tail_calls(scheme_eval)
