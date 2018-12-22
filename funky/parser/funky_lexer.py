import ply.lex as lex

from funky.util import err

class FunkyLexer:

    tokens = [
        # variables and literals
        "IDENTIFIER",
        "NUMBER",
        "FLOAT",
        "CHAR",
        "STRING",

        # math-related operators
        "EQUALS",
        "PLUS",
        "MINUS",
        "TIMES",
        "DIVIDE",
        "POW",

        # miscellaneous operators
        "ARROW",
        "GUARD",

        # brackets
        "OPEN_BRACKET",
        "CLOSE_BRACKET",

        # keywords
        "LET",
        "IN",
        "IF",
        "ELSE",
        "WHERE",
        "MATCH",

        # miscellaneous
        "NEWLINE",
    ]

    t_ignore        = r" " # ignore whitespace.
    t_IDENTIFIER    = r"[A-Za-z][A-za-z0-9_]*"

    def t_NUMBER(self, t):
        r"\d+"
        t.value = int(t.value)
        return t

    def t_FLOAT(self, t):
        r"\d+\.\d+"
        t.value = float(t.value)
        return t

    t_CHAR          = r"'[.]'"
    t_STRING        = r"(\".*?\"|'.*?')"

    t_EQUALS        = r"="
    t_PLUS          = r"\+"
    t_MINUS         = r"-"
    t_TIMES         = r"\*"
    t_DIVIDE        = r"/"
    t_POW           = r"\*\*"

    t_ARROW         = r"->"
    t_GUARD         = r"\|"

    t_OPEN_BRACKET  = r"\("
    t_CLOSE_BRACKET = r"\)"

    t_LET           = r"let"
    t_IN            = r"in"
    t_IF            = r"if"
    t_ELSE          = r"else"
    t_WHERE         = r"where"
    t_MATCH         = r"match"

    t_NEWLINE       = r"\n+"

    def t_error(self, t):
        err("Cannot lex input.") # TODO -- make an exception here.

    def build(self, **kwargs):
        """Build the lexer."""
        self.lexer = lex.lex(module=self, **kwargs)
    
    def do_lex(self, data):
        self.lexer.input(data)
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok: break
            tokens.append(tok)
        return tokens
