"""Fixity resolution for infix expressions. Inspired by the Haskell fixity
resolution algorithm, described at:
    https://prime.haskell.org/wiki/FixityResolution
"""

import logging

from funky.corelang.builtins import BUILTIN_FUNCTIONS
from funky.corelang.sourcetree import UsedVar, FunctionApplication

from funky.parse import FunkySyntaxError
from funky.parse.funky_lexer import FunkyLexer

log = logging.getLogger(__name__)

# The default fixity for an infix function (if it isn't defined explicitly with
# the setfix directive) is assumed to be LEFT ASSOCIATIVE with MAXIMUM
# PRECEDENCE.
DEFAULT_FIXITY = ("leftassoc",  9)

fixities = {
    # imaginary operator -- has a lower precedence than everything else, and is
    # used *exclusively* to kick off the fixity resolution recursive algorithm,
    # This is not a legal operator in Funky code.
    "!!!" : ("nonassoc",  0),

    "or"   :  ("rightassoc",  3),
    "and"  :  ("rightassoc",  4),
    "=="   :  ("nonassoc",    5),
    ">="   :  ("nonassoc",    5),
    ">"    :  ("nonassoc",    5),
    "!="   :  ("nonassoc",    5),
    "<="   :  ("nonassoc",    5),
    "<"    :  ("nonassoc",    5),
    "++"   :  ("rightassoc",  5),
    "-"    :  ("leftassoc",   6),
    "+"    :  ("leftassoc",   6),
    "/"    :  ("leftassoc",   7),
    "%"    :  ("leftassoc",   7),
    "*"    :  ("leftassoc",   7),
    "**"   :  ("rightassoc",  8),
}

def set_fixity(operator, associativity, precedence):
    """Sets the fixity of an operator.
    
    :param operator:      the operator for which you want to set a fixity
    :param associativity: the associativity; either leftassoc, rightassoc, or nonassoc
    :param precedence:    the precedence of the operator
    """
    fixities[operator] = (associativity, precedence)

def get_fixity(operator):
    """Gets the associativity and precedence of an operator.
    
    :param operator: the operator under consideration
    :return:         a tuple (associativity, precedence), where associativity
                     is either "leftassoc", "rightassoc", or "nonassoc", and precedence
                     is an integer
    :rtype:          tuple
    """
    try:
        return fixities[operator]
    except KeyError:
        raise FunkySyntaxError("Invalid operator '{}'.".format(operator))

def resolve_fixity(infix_expr):
    """Performs fixity resolution for an INFIX_EXP from the parser. Infix
    expressions from the parser are 'flat', and are sent here to be converted
    into a tree-like structure that correctly reflects operator precedence and
    associativity.
    
    :param infix_expr: the infix expression from the parser
    :return:           a chain of FunctionApplications equivalent to the infix
                       expression
    """
    log.debug("Resolving fixity for expression '{}'.".format(infix_expr))
    retval = parse_neg("!!!", infix_expr.tokens)[0]
    log.debug("Result was '{}'.".format(retval))
    return retval

def parse_neg(operator, tokens):
    """Function is required to handle negatives."""
    _, minus_precedence = get_fixity("-")
    if tokens[0] == "-":
        fix1, prec1 = get_fixity(operator)
        if prec1 >= minus_precedence:
            raise FunkySyntaxError("Invalid negation.")
        r, rest = parse_neg("-", tokens[1:])
        return parse(operator, FunctionApplication("negate", r),
                     rest)
    else:
        return parse(operator, tokens[0], tokens[1:])

def parse(op1, exp, tokens):
    if not tokens:
        return (exp, [])

    op2 = tokens[0]
    (fix1, prec1), (fix2, prec2) = get_fixity(op1), get_fixity(op2)

    # Case 1: we check for illegal expressions. If op1 and op2 have the
    # same precedence, but they do not have the same associativity, or they are
    # declared to be nonfix, then the expression is illegal.
    if prec1 == prec2 and (fix1 != fix2 or fix1 == "nonassoc"):
        raise FunkySyntaxError("Illegal expression.")

    # Case 2: op1 and op2 are left associative.
    if prec1 > prec2 or (prec1 == prec2 and fix1 == "leftassoc"):
        return (exp, [op2] + tokens[1:])

    # Case 3: op1 and op2 are right associative.
    (r, rest) = parse_neg(op2, tokens[1:])

    if op2 not in BUILTIN_FUNCTIONS:
        op2 = UsedVar(op2)

    return parse(op1, FunctionApplication(FunctionApplication(op2, exp), r), rest)
