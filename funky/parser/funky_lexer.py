"""Lexical analyser for the funky programming language. Lexical analysis
involves taking the source code as a raw string and splitting it down into
'tokens' for easier parsing later.

The lexical analysis phase for funky consists of two parts: the first involves
taking the raw source and splitting it down into tokens; the second involves
taking the result of the first stage and inserting any implicit braces. The way
that we handle this is very similar to the 'layout' rule in Haskell.
"""

import ply.lex as lex

from funky.util import err
from funky.parser import FunkyLexingError

class FunkyLexer:
    """PLY lexer for funky. This performs the first stage of lexical analysis
    on the source code -- i.e. breaks down the source into "tokens" where a
    token represents the basic unit of meaning.
    """

    # Reserved keywords -- variables may not have these names.
    reserved = {
        "module"   :  "MODULE",
        "import"   :  "IMPORT",
        "as"       :  "AS",
        "newtype"  :  "NEWTYPE",
        "let"      :  "LET",
        "in"       :  "IN",
        "if"       :  "IF",
        "then"     :  "THEN",
        "else"     :  "ELSE",
        "where"    :  "WHERE",
        "match"    :  "MATCH",
        "of"       :  "OF",
        "infix"    :  "INFIX",
        "infixl"   :  "INFIXL",
        "infixr"   :  "INFIXR",
    }

    # All the tokens known to the lexer.
    tokens = [

        # structural
        "WHITESPACE",

        # 'control' characters
        "BACKTICK",
        "COMMA",
        "TYPESIG",
        "CONSTRUCTOR",
        "LAMBDA",
        "PIPE",
        "WILDCARD",
        "ARROW",
        "ENDSTATEMENT",

        # literals
        "FLOAT",
        "INTEGER",
        "BOOL",
        "CHAR",
        "STRING",

        # math-related operators
        "EQUALITY",
        "INEQUALITY",
        "LESS",
        "LEQ",
        "GREATER",
        "GEQ",
        "EQUALS",
        "POW",
        "PLUS",
        "MINUS",
        "TIMES",
        "DIVIDE",

        # brackets
        "OPEN_PAREN",
        "CLOSE_PAREN",
        "OPEN_SQUARE",
        "CLOSE_SQUARE",
        "OPEN_BRACE",
        "CLOSE_BRACE",

        # identifiers and labels
        "IDENTIFIER",
        "TYPENAME",
    ] + list(reserved.values())

    # Ignore spaces and tabs (unless they appear in the context of another
    # lexeme)
    t_ignore        =  "\t"

    at_line_start   = True

    # Comments are the same as they are in python -- this function returns
    # nothing since comments are ignored.
    def t_COMMENT(self, t):
        r"[ ]*\#[^\n]*"
        pass

    def t_WHITESPACE(self, t):
        r"[ ]+"
        # we only care about whitespace if it's at the start of a line
        if self.at_line_start:
            t.value = t.value.count(" ") # level of indentation = number of spaces
            return t

    def t_NEWLINE(self, t):
        r"\n+"
        self.at_line_start = True
        t.lexer.lineno += len(t.value)

    # Regexes for the control characters.
    t_BACKTICK      =  r"`"
    t_COMMA         =  r","
    t_TYPESIG       =  r"::"
    t_CONSTRUCTOR   =  r":"
    t_LAMBDA        =  r"\\"
    t_PIPE          =  r"\|"
    t_WILDCARD      =  r"_"
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

    t_CHAR          =  r"'[.]'"
    t_STRING        =  r"(\".*?\"|'.*?')"

    # Math operators.
    t_EQUALITY      =  r"=="
    t_INEQUALITY    =  r"!="
    t_LESS          =  r"<"
    t_LEQ           =  r"<="
    t_GREATER       =  r">"
    t_GEQ           =  r">="
    t_EQUALS        =  r"="
    t_POW           =  r"\*\*"
    t_PLUS          =  r"\+"
    t_MINUS         =  r"-"
    t_TIMES         =  r"\*"
    t_DIVIDE        =  r"/"

    # Brackets.
    t_OPEN_PAREN    =  r"\("
    t_CLOSE_PAREN   =  r"\)"
    t_OPEN_SQUARE   =  r"\["
    t_CLOSE_SQUARE  =  r"\]"
    t_OPEN_BRACE    =  r"\{"
    t_CLOSE_BRACE   =  r"\}"

    # An identifier -- checks for keywords.
    def t_IDENTIFIER(self, t):
         r"[a-z][A-Za-z0-9_]*"
         t.type = self.reserved.get(t.value, "IDENTIFIER") # Check for keywords
         return t

    # Typenames are always capitalised, as in Haskell.
    t_TYPENAME      = r"[A-Z][A-Za-z]*"

    def t_error(self, t):
        err("Cannot lex input.") # TODO -- make an exception here.

    def build(self, **kwargs):
        """Build the lexer."""
        self.lexer = lex.lex(module=self, **kwargs)
    
    def do_lex(self, source, *args, **kwargs):
        self.lexer.input(source, *args, **kwargs)

        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok: break

            self.at_line_start = False
            tokens.append(tok)

        return tokens

class IndentationLexer:
    """Indentation lexer. This performs the second stage of lexical analysis --
    here, we find where braces and semicolons have been omitted (implicit
    braces inferred from indentation) and insert them as literal characters
    into the token stream.
    """

    def __init__(self, lexer):
        self.lexer = lexer
        self.ind_stack = []
        self.new_tokens = []
        self.source = ""

    def input(self, source, *args, **kwargs):
        self.source = source
        self.orig_tokens = self.lexer.do_lex(source, *args, **kwargs)
        self.new_tokens = self._insert_implicit_tokens(self.orig_tokens)

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
        new_tokens = []

        ind_stack = []
        
        i = 0
        while i < len(tokens):
            tok = tokens[i]
            if tok.type in ["WHERE", "LET", "OF"] and \
               tokens[i + 1].type != "OPEN_BRACE":
                j = i + 1
                while tokens[j].type == "WHITESPACE":
                    j += 1
                ind_stack.append(self._find_column(tokens[j]))
                new_tokens.append(tok)
                new_tokens.append(self._make_token("OPEN_BRACE", value="{"))
            elif tok.type == "WHITESPACE":
                if ind_stack:
                    if tok.value == ind_stack[-1]:
                        new_tokens.append(self._make_token("ENDSTATEMENT", value=";"))
                    elif tok.value < ind_stack[-1]:
                        new_tokens.append(self._make_token("CLOSE_BRACE", value="}"))
                        ind_stack.pop()
                        continue
            else:
                new_tokens.append(tok)

            i += 1

        while ind_stack:
            new_tokens.append(self._make_token("CLOSE_BRACE", value="}"))
            ind_stack.pop()

        return new_tokens

    def _make_token(self, type, value=None, lineno=None, lexpos=None):
        tok = lex.LexToken()
        tok.type = type
        tok.value = value
        tok.lineno = 0
        tok.lexpos = 0
        return tok

    def _find_column(self, token):
        """Given the source string and a token from it (found by the lexer), gets
        the column in the line that the token appeared in. This is required for
        layout ruling.
        """
        line_start = self.source.rfind("\n", 0, token.lexpos) + 1
        retval = (token.lexpos - line_start)
        return retval
