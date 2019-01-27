"""Lexical analyser for the funky programming language. Lexical analysis
involves taking the source code as a raw string and splitting it down into
'tokens' for easier parsing later.

The lexical analysis phase for funky consists of two parts: the first involves
taking the raw source and splitting it down into tokens; the second involves
taking the result of the first stage and inserting any implicit braces. The way
that we handle this is very similar to the 'layout' rule in Haskell.
"""

import logging
import ply.lex as lex

from funky.parse import FunkyLexingError

log = logging.getLogger(__name__)

class FunkyLexer:
    """PLY lexer for funky. This performs the first stage of lexical analysis
    on the source code -- i.e. breaks down the source into "tokens" where a
    token represents the basic unit of meaning.
    """

    # Reserved keywords -- variables are not permitted to have these names.
    reserved = [
        "as", "else", "if", "import", "in", "lambda", "leftassoc", "let",
        "match", "module", "newcons", "newtype", "nonassoc", "of",
        "rightassoc", "setfix", "then", "where",
    ]
    reserved = {k : k.upper() for k in reserved}

    # All the tokens known to the lexer.
    tokens = [
        "WHITESPACE",

        "BACKTICK", "COMMA", "TYPESIG", "PIPE", "ARROW", "ENDSTATEMENT",

        "FLOAT", "INTEGER", "BOOL", "CHAR", "STRING",

        "EQUALITY", "INEQUALITY", "LESS", "LEQ", "GREATER", "GEQ", "EQUALS",
        "POW", "PLUS", "MINUS", "TIMES", "DIVIDE", "AND", "OR",
        "LIST_CONSTRUCTOR",

        "OPEN_PAREN", "CLOSE_PAREN", "OPEN_SQUARE", "CLOSE_SQUARE",
        "OPEN_BRACE", "CLOSE_BRACE",

        "IDENTIFIER", "TYPENAME",
    ] + list(reserved.values())

    # Ignore tabs.
    t_ignore        =  "\t"

    # True if we are at the start of the line -- in this case, we consider any
    # whitespace to be indentation. False otherwise.
    at_line_start   = True

    # Comments are the same as they are in python -- this function returns
    # nothing since comments are ignored.
    def t_COMMENT(self, t):
        r"[ ]*\#[^\n]*"
        pass

    # We only care about whitespace if it's at the start of a line.
    def t_WHITESPACE(self, t):
        r"[ ]+"
        if self.at_line_start:
            t.value = len(t.value)
            return t

    # Newlines increment the line number.
    def t_NEWLINE(self, t):
        r"\n+"
        self.at_line_start = True

    # Regexes for the control characters.
    t_BACKTICK      =  r"`"
    t_COMMA         =  r","
    t_TYPESIG       =  r"::"
    t_PIPE          =  r"\|"
    t_ARROW         =  r"->"
    t_ENDSTATEMENT  =  r";"

    # Literals:
    def t_FLOAT(self, t):
        r"\d+\.\d+"
        t.value = float(t.value)
        return t

    def t_INTEGER(self, t):
        r"\d+"
        t.value = int(t.value)
        return t

    def t_BOOL(self, t):
        r"(True|False)"
        t.value = t.value == "True"
        return t

    def t_CHAR(self, t):
        r"'.'"
        t.value = t.value[1:-1]
        return t

    def t_STRING(self, t):
        r"(\".*?\"|'.*?')"
        t.value = t.value[1:-1]
        return t

    # Math operators.
    t_EQUALITY          =  r"=="
    t_INEQUALITY        =  r"!="
    t_LESS              =  r"<"
    t_LEQ               =  r"<="
    t_GREATER           =  r">"
    t_GEQ               =  r">="
    t_EQUALS            =  r"="
    t_POW               =  r"\*\*"
    t_PLUS              =  r"\+"
    t_MINUS             =  r"-"
    t_TIMES             =  r"\*"
    t_DIVIDE            =  r"/"
    t_AND               =  r"&&"
    t_OR                =  r"\|\|"
    t_LIST_CONSTRUCTOR  =  r":"

    # Brackets.
    t_OPEN_PAREN    =  r"\("
    t_CLOSE_PAREN   =  r"\)"
    t_OPEN_SQUARE   =  r"\["
    t_CLOSE_SQUARE  =  r"\]"
    t_OPEN_BRACE    =  r"\{"
    t_CLOSE_BRACE   =  r"\}"

    # An identifier -- checks for keywords.
    def t_IDENTIFIER(self, t):
         r"([a-z][A-Za-z0-9_]*|_)"
         t.type = self.reserved.get(t.value, "IDENTIFIER")
         return t

    # Typenames are always capitalised, as in Haskell.
    t_TYPENAME  =  r"[A-Z][A-Za-z]*"

    def t_error(self, t):
        raise FunkyLexingError(
            "Lexing failed on character '{}'.".format(t.value[0]))

    def build(self, **kwargs):
        """Build the lexer."""
        log.debug("Using PLY to build the lexer.")
        self.lexer = lex.lex(module=self, **kwargs)
        log.debug("Lexer built.")

    def do_lex(self, source, *args, **kwargs):
        log.info("Performing basic lexing of the source.")
        self.lexer.input(source, *args, **kwargs)

        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok: break

            self.at_line_start = False
            tokens.append(tok)

        log.info("Completed basic lexing.")
        return tokens

class IndentationLexer:
    """Indentation lexer. This performs the second stage of lexical analysis --
    here, we find where braces and semicolons have been omitted (implicit
    braces inferred from indentation) and insert them as literal characters
    into the token stream.
    """

    def __init__(self, lexer):
        self.lexer       =  lexer
        self.new_tokens  =  []
        self.source      =  ""

    def input(self, source, *args, **kwargs):
        self.source       =  source
        self.orig_tokens  =  self.lexer.do_lex(source, *args, **kwargs)
        self.new_tokens   =  self._insert_implicit_tokens(self.orig_tokens)

    def __iter__(self):
        return self

    def __next__(self):
        tok = self.token()
        if not tok:
            raise StopIteration()
        return tok

    def token(self):
        if self.new_tokens:
            return self.new_tokens.pop(0)

    def _insert_implicit_tokens(self, tokens):
        """Inserts explicit braces into a token stream containing omitted
        braces.
        """
        log.debug("Using the layout rule to convert indentation to explicit "
                  "braces.")
        new_tokens, ind_stack = [], []

        i = 0
        while i < len(tokens):
            tok = tokens[i]
            if tok.type in ["WHERE", "LET", "OF"] and \
               tokens[i + 1].type != "OPEN_BRACE":
                j = i + 1
                while tokens[j].type == "WHITESPACE":
                    tokens.pop(j)
                ind_stack.append(self._find_column(tokens[j]))
                new_tokens.append(tok)
                new_tokens.append(self._make_token("OPEN_BRACE", value="{"))
            elif tok.type == "WHITESPACE":
                if ind_stack:
                    if tok.value == ind_stack[-1]:
                        new_tokens.append(self._make_token("ENDSTATEMENT",
                                                           value=";"))
                    elif tok.value < ind_stack[-1]:
                        new_tokens.append(self._make_token("CLOSE_BRACE",
                                                           value="}"))
                        ind_stack.pop()
                        continue
            else:
                new_tokens.append(tok)

            i += 1

        while ind_stack:
            new_tokens.append(self._make_token("CLOSE_BRACE", value="}"))
            ind_stack.pop()

        logging.debug("Finished adding explicit braces.")
        return new_tokens

    def _make_token(self, typ, value=None, lineno=None, lexpos=None):
        """Creates a token with the given arguments.

        Input:
            type   -- token type.
            value  -- token value
            lineno -- line number.
            lexpos -- lexing position.
        
        Returns:
            a token with the given arguments.
        """
        tok         =  lex.LexToken()
        tok.type    =  typ
        tok.value   =  value
        tok.lineno  =  0
        tok.lexpos  =  0
        return tok

    def _find_column(self, token):
        """Given the source string and a token from it (found by the lexer),
        gets the column in the line that the token appeared in. This is
        required for layout ruling.

        Input:
            token -- a token.
        
        Returns:
            an integer representing the column in the line where the token
            appeared.
        """
        line_start = self.source.rfind("\n", 0, token.lexpos) + 1
        return (token.lexpos - line_start)
