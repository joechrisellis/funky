"""Contains code for the lexical analysis component of the compiler.  Lexical
analysis involves taking the source code as a raw string and splitting it down
into 'tokens'. These are easier to parse later.
"""
from enum import Enum, auto
import re

from . import FunkyError

class InvalidSourceException(FunkyError):
    """Raised when the source code cannot be lexed."""
    pass

class TokenType(Enum):
    """Enumeration used to identify the type of a token."""
    IDENTIFIER = auto()
    INTEGER    = auto()
    KEYWORD    = auto()
    OPERATOR   = auto()
    SEPARATOR  = auto()
    STRING     = auto()

    END        = auto() # <- end input marker used in parsing

regexes = [
    # drop all whitespace and comments
    (None, re.compile(r"\s+")),
    (None, re.compile(r"#.*")),

    (TokenType.OPERATOR, re.compile(r"=")),
    (TokenType.SEPARATOR, re.compile(r"\(")),
    (TokenType.SEPARATOR, re.compile(r"\)")),
    (TokenType.SEPARATOR, re.compile(r"\|")),
    (TokenType.SEPARATOR, re.compile(r"\n+")),

    (TokenType.OPERATOR, re.compile(r"\+")),
    (TokenType.OPERATOR, re.compile(r"-")),
    (TokenType.OPERATOR, re.compile(r"\*")),
    (TokenType.OPERATOR, re.compile(r"/")),
    (TokenType.OPERATOR, re.compile(r"%")),
    (TokenType.OPERATOR, re.compile(r"<=")),
    (TokenType.OPERATOR, re.compile(r"<")),
    (TokenType.OPERATOR, re.compile(r">=")),
    (TokenType.OPERATOR, re.compile(r">")),
    (TokenType.OPERATOR, re.compile(r"==")),
    (TokenType.OPERATOR, re.compile(r"!=")),
    (TokenType.OPERATOR, re.compile(r"and")),
    (TokenType.OPERATOR, re.compile(r"or")),
    (TokenType.OPERATOR, re.compile(r"not")),

    (TokenType.KEYWORD, re.compile(r"let")),
    (TokenType.KEYWORD, re.compile(r"in")),
    (TokenType.KEYWORD, re.compile(r"if")),
    (TokenType.KEYWORD, re.compile(r"then")),
    (TokenType.KEYWORD, re.compile(r"else")),
    (TokenType.KEYWORD, re.compile(r"lam")),

    (TokenType.INTEGER, re.compile(r"[0-9]+")),
    (TokenType.STRING, re.compile(r"\".*\"")),
    (TokenType.STRING, re.compile(r"'.*'")),
    (TokenType.IDENTIFIER, re.compile(r"[A-Za-z][A-Za-z_0-9]*")),
]

def lex(source, regexes):
    """Converts the given source code into tokens given a list of token
    regexes.

    Input:
        source  -- the raw source code
        regexes -- a list of tuples (TokenType, regex)

    Returns:
        a list of tokens (TokenType, value)
    """
    cursor, tokens = 0, []
    while cursor < len(source):
        for regex in regexes:
            tag, pattern = regex
            match = pattern.match(source, cursor)
            if match:
                if tag:
                    tokens.append((tag, match.group(0)))
                cursor = match.end(0)
                break
        else:
            raise InvalidSourceException(
                "Invalid character '{}'".format(source[cursor]))

    tokens.append((TokenType.END, None))
    return tokens
