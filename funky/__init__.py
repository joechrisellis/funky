
class FunkyError(Exception):
    """Base class for all funky errors."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

from funky.lexer import Token, TokenType
from funky.parsers import ContextFreeGrammar, EPSILON
from funky.parsers.grammar_generator import generate_grammar

FUNKY_GRAMMAR = generate_grammar("prog", f"""
prog         :: functionlist;

functionlist :: function functionlist;
functionlist :: {EPSILON};

function     :: <"IDENTIFIER"> arglist guard <"OPERATOR", "="> expr;

guard        :: <"SEPARATOR", "|"> expr;
guard        :: {EPSILON};

arglist      :: arg arglist;
arglist      :: {EPSILON};

arg          :: <"IDENTIFIER">;
arg          :: <"INTEGER">;
arg          :: <"STRING">;

expr         :: <"INTEGER">;
expr         :: <"IDENTIFIER">;
""")

example_program = """
factorial n | 0 = 1
factorial n | 1 = n
"""
