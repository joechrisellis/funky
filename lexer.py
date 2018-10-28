from enum import Enum
import re

class TokenType(Enum):
    KEYWORD = 1
    OPERATOR = 2
    SEPARATOR = 3
    LITERAL = 4
    IDENTIFIER = 5

regexes = [
    # drop all whitespace and comments
    (None, re.compile(r"\s+")),
    (None, re.compile(r"#.*")),

    (TokenType.OPERATOR, re.compile(r"=")),
    (TokenType.SEPARATOR, re.compile(r"\(")),
    (TokenType.SEPARATOR, re.compile(r"\)")),
    (TokenType.SEPARATOR, re.compile(r"\n+")),
    (TokenType.OPERATOR, re.compile(r"\+")),
    (TokenType.OPERATOR, re.compile(r"-")),
    (TokenType.OPERATOR, re.compile(r"\*")),
    (TokenType.OPERATOR, re.compile(r"/")),
    (TokenType.OPERATOR, re.compile(r"<=")),
    (TokenType.OPERATOR, re.compile(r"<")),
    (TokenType.OPERATOR, re.compile(r">=")),
    (TokenType.OPERATOR, re.compile(r">")),
    (TokenType.OPERATOR, re.compile(r"==")),
    (TokenType.OPERATOR, re.compile(r"!=")),
    (TokenType.OPERATOR, re.compile(r"and")),
    (TokenType.OPERATOR, re.compile(r"or")),
    (TokenType.OPERATOR, re.compile(r"not")),

    (TokenType.KEYWORD, re.compile(r"if")),
    (TokenType.KEYWORD, re.compile(r"then")),
    (TokenType.KEYWORD, re.compile(r"else")),
    (TokenType.KEYWORD, re.compile(r"lam")),

    (TokenType.LITERAL, re.compile(r"[0-9]+")),
    (TokenType.IDENTIFIER, re.compile(r"[A-Za-z][A-Za-z_0-9]*")),
]

def lex(source, regexes):
    """Converts the given source code into tokens given a list of token
    regexes.
    
    Input:
        source  -- the raw source code
        regexes -- a list of tuples (TokenType, regex)

    Returns: a list of tokens (TokenType, value)
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
            print("Invalid character: {}".format(source[cursor]))
            return None
    return tokens
