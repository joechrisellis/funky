"""Fixity resolution for infix expressions. Inspired by the Haskell fixity
resolution algorithm, described at:
    https://prime.haskell.org/wiki/FixityResolution
"""

from funky.core.intermediate import BinOpApplication, UnaryOpApplication

# TODO: make sure these are consistent with what appears in the lexer!
precedence  =  (
    ("nonassoc", "!!!"), # Imaginary operator!
    ("nonassoc", "=="),
    ("left", "<", "<=", ">", ">="),
    ("left", "+", "-"),
    ("left", "*", "/"),
    ("right", "**"),
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
    return None

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
    print(retval)
    return retval

def parse_neg(operator, tokens):
    """Function is required to handle negatives."""
    _, minus_precedence = get_precedence("-")
    if tokens[0] == "-":
        fix1, prec1 = get_precedence(operator)
        if prec1 >= minus_precedence:
            raise ValueError("Invalid negation.")
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
        raise ValueError("Invalid expression.")

    # Case 2: op1 and op2 are left associative.
    if prec1 > prec2 or (prec1 == prec2 and fix1 == "left"):
        return (exp, [op2] + tokens[1:])

    # Case 3: op1 and op2 are right associative.
    (r, rest) = parse_neg(op2, tokens[1:])

    return parse(op1, BinOpApplication(exp, op2, r), rest)
