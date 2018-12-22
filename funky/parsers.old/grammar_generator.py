"""Provides a function to generate a ContextFreeGrammar object from a string
string. This makes it easy for the programmer to define new grammars; they can
write the grammar down as a string instead of as a formatted Python dictionary.
The grammar strings are also significantly easier to read.
"""
import funky.lexer as lexer
from funky.lexer import Token, TokenType
from funky.parsers import ContextFreeGrammar, EPSILON
from funky.parsers.llparser import LLParser

grammar_for_grammars = ContextFreeGrammar("G", {
    "G"               : [["definitionlist"]],
    "definitionlist"  : [["definition", "definitionlist"],
                         [EPSILON]],
    "definition"      : [["nonterminal", Token(TokenType.OPERATOR, "::"), "symbols", Token(TokenType.SEPARATOR, ";")]],
    "symbols"         : [["symbol", "symbols"],
                         [EPSILON]],
    "symbol"          : [["terminal"],
                         ["nonterminal"]],
    "nonterminal"     : [[Token(TokenType.IDENTIFIER)]],
    "terminal"        : [[Token(TokenType.OPERATOR, "<"), Token(TokenType.STRING), "tokenvalue", Token(TokenType.OPERATOR, ">")]],
    "tokenvalue"      : [[Token(TokenType.SEPARATOR, ","), Token(TokenType.STRING)],
                         [EPSILON]],
})

def generate_grammar(start_symbol, grammar_string):
    """Given a start symbol and a grammar string, generates the corresponding
    ContextFreeGrammar object. This function works by parsing the given string
    using a pre-defined grammar for valid grammar strings, then traverses the
    parse tree to convert it into a ContextFreeGrammar object.

    Input:
        start_symbol   -- the start symbol of the grammar.
        grammar_string -- the grammar string.

    Returns:
        a ContextFreeGrammar object representing the grammar given by the user.
    """

    tokens = lexer.lex(grammar_string, lexer.regexes)
    parser = LLParser(grammar_for_grammars)

    ast = parser.parse(tokens)
    the_grammar = {}

    def populate_grammar(ast, nonterminal=None):
        if ast.value == "G":
            populate_grammar(ast.children[0])

        elif ast.value == "definitionlist" and ast.children:
            populate_grammar(ast.children[0])
            populate_grammar(ast.children[1])

        elif ast.value == "definition":
            nt = ast.children[0].children[0].value.token_value
            the_grammar[nt] = the_grammar.get(nt, []) + [[]]
            populate_grammar(ast.children[2], nonterminal=nt)

        elif ast.value == "symbols" and ast.children:
            populate_grammar(ast.children[0], nonterminal=nonterminal)
            populate_grammar(ast.children[1], nonterminal=nonterminal)

        elif ast.value == "symbol":
            populate_grammar(ast.children[0], nonterminal=nonterminal)

        elif ast.value == "nonterminal":
            the_grammar[nonterminal][-1].append(ast.children[0].value.token_value)

        elif ast.value == "terminal":
            type_token = ast.children[1].value
            token_type = getattr(TokenType, type_token.token_value[1:-1])
            
            token_value = None
            if len(ast.children[2].children) >= 1:
                value_token = ast.children[2].children[1].value
                token_value = value_token.token_value[1:-1]
            the_grammar[nonterminal][-1].append(Token(token_type, token_value))

    populate_grammar(ast)

    return ContextFreeGrammar(start_symbol, the_grammar)
