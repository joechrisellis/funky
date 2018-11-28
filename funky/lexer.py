"""Contains code for the lexical analysis component of the compiler.  Lexical
analysis involves taking the source code as a raw string and splitting it down
into 'tokens'. These are easier to parse later.
"""
from enum import Enum, auto
import re

from funky import FunkyError

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

class Token:
    
    def __init__(self, token_type, token_value=None):
        self.token_type = token_type
        self.token_value = token_value

    def has_value(self):
        """Returns true if this token has a value associated with it, false
        otherwise.
        """
        return self.token_value is not None

    def strip_value(self):
        """Returns a new token object with the value stripped."""
        return Token(self.token_type, None)

    def __eq__(self, other):
        # can only compare two tokens, and different types mean that the tokens
        # are absolutely not equal
        if not isinstance(other, Token) or \
           self.token_type != other.token_type: 
            return False

        # if either token has the value None, they are equal (given that they
        # are assured to have the same type now)
        if self.token_value is None or other.token_value is None:
            return True
        return self.token_value == other.token_value

    def __repr__(self):
        return "<{}: {}>".format(self.token_type, self.token_value)

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash((self.token_type, self.token_value))

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
                    tokens.append(Token(tag, match.group(0)))
                cursor = match.end(0)
                break
        else:
            raise InvalidSourceException(
                "Invalid character '{}'".format(source[cursor]))

    tokens.append(Token(TokenType.END))
    return tokens
