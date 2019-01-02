"""Fixity resolution for infix expressions. Inspired by the Haskell fixity
resolution algorithm, described at:
    https://prime.haskell.org/wiki/FixityResolution
"""

from funky.parser import FunkySyntaxError
from funky.parser.ast import BinOpApplication, UnaryOpApplication
from funky.parser.funky_lexer import FunkyLexer

def _rmb(s):
    """Removes backslashes from a string."""
    return s.replace("\\", "")

precedence  =  (
    # imaginary operator -- has a lower precedence than everything else, and is
    # used *exclusively* to kick off the fixity resolution recursive algorith,
    # This is not a legal operator in Funky code.
    ("nonassoc", "!!!"),

    # Remove backslashes from the lexer regexes for operators. This gets the
    # 'raw' operator string. If the operator lexemes are changed in the lexer,
    # the change is automatically propagated to here.
    ("nonassoc", _rmb(FunkyLexer.t_EQUALITY)),
    ("left",     _rmb(FunkyLexer.t_LESS), _rmb(FunkyLexer.t_LEQ),
                 _rmb(FunkyLexer.t_GREATER), _rmb(FunkyLexer.t_GEQ)),
    ("left",     _rmb(FunkyLexer.t_PLUS), _rmb(FunkyLexer.t_MINUS)),
    ("left",     _rmb(FunkyLexer.t_TIMES), _rmb(FunkyLexer.t_DIVIDE)),
    ("right",    _rmb(FunkyLexer.t_POW)),
)

def get_precedence(operator):
    """Gets the associativity and precedence of an operator.
    
    Input:
        operator -- the operator to be considered.
    
    Output:
        a tuple (associativity, precedence), where associativity is either
        "left", "right", or "nonassoc", and precedence is an integer.
    """
    for i, pclass in enumerate(precedence):
        if operator in pclass:
            return (pclass[0], i)
    raise FunkySyntaxError("Invalid operator '{}'.".format(operator))

def resolve_fixity(infix_expr):
    """Performs fixity resolution for an INFIX_EXP from the parser. Infix
    expressions from the parser are 'flat', and are sent here to be converted
    into a tree-like structure that correctly reflects operator precedence and
    associativity.
    
    Input:
        infix_expr -- the infix expression from the parser.

    Output:
        a BinOpApplication or UnaryOpApplication representing the infix
        expression.
    """
    retval = parse_neg("!!!", infix_expr.tokens)[0]
    return retval

def parse_neg(operator, tokens):
    """Function is required to handle negatives."""
    _, minus_precedence = get_precedence("-")
    if tokens[0] == "-":
        fix1, prec1 = get_precedence(operator)
        if prec1 >= minus_precedence:
            raise FunkySyntaxError("Invalid negation.")
        r, rest = parse_neg("-", tokens[1:])
        return parse(operator, UnaryOpApplication("-", r), rest)
    else:
        return parse(operator, tokens[0], tokens[1:])

def parse(op1, exp, tokens):
    if not tokens:
        return (exp, [])

    op2 = tokens[0]
    (fix1, prec1), (fix2, prec2) = get_precedence(op1), get_precedence(op2)

    # Case 1: we check for illegal expressions. If op1 and op2 have the
    # same precedence, but they do not have the same associativity, or they are
    # declared to be nonfix, then the expression is illegal.
    if prec1 == prec2 and (fix1 != fix2 or fix1 == "nonassoc"):
        raise FunkySyntaxError("Illegal expression.")

    # Case 2: op1 and op2 are left associative.
    if prec1 > prec2 or (prec1 == prec2 and fix1 == "left"):
        return (exp, [op2] + tokens[1:])

    # Case 3: op1 and op2 are right associative.
    (r, rest) = parse_neg(op2, tokens[1:])

    return parse(op1, BinOpApplication(exp, op2, r), rest)
