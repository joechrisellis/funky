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

from funky.util.color import *
from funky.parse import FunkyLexingError

log = logging.getLogger(__name__)

class FunkyLexer:
    """PLY lexer for funky. This performs the first stage of lexical analysis
    on the source code -- i.e. breaks down the source into "tokens" where a
    token represents the basic unit of meaning.
    """

    # Reserved keywords -- variables are not permitted to have these names.
    reserved = [
        "and", "else", "given", "if", "import", "in", "lambda", "leftassoc",
        "let", "match", "module", "newtype", "nonassoc", "or", "rightassoc",
        "setfix", "with", "on",
    ]
    reserved = {k : k.upper() for k in reserved}

    # All the tokens known to the lexer.
    tokens = [
        "WHITESPACE",

        "TILDE", "PIPE", "ARROW", "ENDSTATEMENT",

        "FLOAT", "INTEGER", "BOOL", "STRING",

        "EQUALITY", "INEQUALITY", "LESS", "LEQ", "GREATER", "GEQ", "EQUALS",
        "FPOW", "IPOW", "CONCAT", "PLUS", "MINUS", "TIMES", "DIVIDE", "MODULO",

        "OPEN_PAREN", "CLOSE_PAREN",
        "OPEN_BRACE", "CLOSE_BRACE",

        "IDENTIFIER", "TYPENAME",
    ] + list(reserved.values())

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

    # Tabs should be ignored, except if they are used for indentation. In
    # Funky, SPACES are used for indentation -- throw an error if tabs are
    # used.
    def t_TAB(self, t):
        r"\t+"
        if self.at_line_start:
            raise FunkyLexingError("Use spaces to indent your code, not tabs.")

    # Newlines increment the line number.
    def t_NEWLINE(self, t):
        r"\n+"
        self.at_line_start = True
        t.lineno += len(t.value)

    # Regexes for the control characters.
    t_TILDE         =  r"~"
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

    def t_STRING(self, t):
        r"(\".*?\"|'.*?')"
        t.value = t.value[1:-1]
        return t

    # Math operators.
    t_EQUALITY    =  r"=="
    t_INEQUALITY  =  r"!="
    t_LESS        =  r"<"
    t_LEQ         =  r"<="
    t_GREATER     =  r">"
    t_GEQ         =  r">="
    t_EQUALS      =  r"="
    t_FPOW        =  r"\*\*"
    t_IPOW        =  r"\^"
    t_CONCAT      =  r"\+\+"
    t_PLUS        =  r"\+"
    t_MINUS       =  r"-"
    t_TIMES       =  r"\*"
    t_DIVIDE      =  r"/"
    t_MODULO      =  r"%"

    # Brackets.
    t_OPEN_PAREN    =  r"\("
    t_CLOSE_PAREN   =  r"\)"
    t_OPEN_BRACE    =  r"\{"
    t_CLOSE_BRACE   =  r"\}"

    # An identifier -- checks for keywords.
    def t_IDENTIFIER(self, t):
         r"([a-z][A-Za-z0-9_]*|_)"
         t.type = self.reserved.get(t.value, "IDENTIFIER")
         return t

    # Typenames are always capitalised, as in Haskell.
    t_TYPENAME  =  r"[A-Z][A-Za-z0-9]*"

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

    def __init__(self, lexer, dump_pretty=False, dump_lexed=False):
        self.lexer        =  lexer
        self.new_tokens   =  []
        self.source       =  ""
        self.dump_pretty  =  dump_pretty
        self.dump_lexed   =  dump_lexed

    def input(self, source, *args, **kwargs):
        self.source       =  source
        self.orig_tokens  =  self.lexer.do_lex(source, *args, **kwargs)
        self.new_tokens   =  self._disambiguate(self.orig_tokens)

        if self.dump_pretty:
            print(cblue("## PRETTIFIED SOURCE"))
            pprint_tokens(self.orig_tokens)
            print("")

        if self.dump_lexed:
            print(cblue("## DUMPED LEXED SOURCE"))
            pprint_tokens(self.new_tokens)
            print("")

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

    def _disambiguate(self, tokens):
        """Inserts explicit braces into a token stream containing omitted
        braces, disambiguating the code.

        :param tokens list: a list of tokens from the first-pass lexer
        :return:            a new list of tokens with explicit braces inserted
        """
        log.debug("Using the layout rule to convert indentation to explicit "
                  "braces.")
        new_tokens, ind_stack = [], []

        i = 0
        while i < len(tokens):
            tok = tokens[i]
            if tok.type in ["WITH", "LET", "ON"] and \
               tokens[i + 1].type != "OPEN_BRACE":
                j = i + 1
                while tokens[j].type == "WHITESPACE":
                    j += 1
                ind_stack.append(self._find_column(tokens[j]))
                new_tokens.append(tok)
                new_tokens.append(self._make_token("OPEN_BRACE", value="{"))
                i = j
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
                i += 1
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

        :param type:   token type
        :param value:  token value
        :param lineno: line number
        :param lexpos: lexing position
        :return:       a token with the given arguments
        :rtype:        Token
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

        :param token: a token
        :return:      an integer representing the column in the line where the
                      token appeared.
        """
        line_start = self.source.rfind("\n", 0, token.lexpos) + 1
        return (token.lexpos - line_start)

def pprint_tokens(tokens):
    indentation, first = 0, True
    for token in tokens:
        s = colored_str(token)
        
        if token.type == "CLOSE_BRACE":
            indentation -= 4
            first = True
            print("")
            print(" " * indentation + s, end="")
        elif token.type == "OPEN_BRACE":
            indentation += 4
            first = True
            print(" " + s)
            print(" " * indentation, end="")
        elif token.type == "ENDSTATEMENT":
            first = True
            print(s, end="")
            print("\n" + " " * indentation, end="")
        else:
            if first:
                print(s, end="")
            else:
                print(" " + s, end="")
            first = False

def colored_str(token):
    """Given a token from the lexer, gets its coloured string representation.
    
    """
    colors = {
        "EQUALS"    :  COLOR_EQUALS,
        "TYPENAME"  :  COLOR_TYPENAME,
    }

    colors.update({k : COLOR_CONSTANT for k in [
        "STRING",
        "INTEGER",
        "FLOAT",
        "BOOL",
    ]})

    # make all keywords yellow
    colors.update({k.upper() : COLOR_KEYWORD for k in FunkyLexer.reserved})

    # make all operators/misc symbols violet
    colors.update({k : COLOR_OPERATOR for k in [
        "EQUALITY",
        "INEQUALITY",
        "LESS",
        "LEQ",
        "GREATER",
        "GEQ",
        "EQUALS",
        "POW",
        "CONCAT",
        "PLUS",
        "MINUS",
        "TIMES",
        "DIVIDE",
        "MODULO",
        "TILDE",
        "PIPE",
        "ARROW",
    ]})

    if token.type == "WHITESPACE":
        return "\n" + " " * token.value

    try:
        v = str(token.value)
        if token.type == "STRING": # <- rewrap it with quotes
            v = "'{}'".format(v)
        return colors[token.type](v)
    except KeyError:
        return str(token.value)
