"""Control flow for the compiler."""
import sys

from funky.util import err
import funky.lexer as lexer
import funky.parsers as parsers
import funky.parsers.llparser as llparser

test_grammar = parsers.ContextFreeGrammar("E", {
    "E" : [["T", "E'"]],
    "E'" : [["+", "T", "E'"], [parsers.EPSILON]],
    "T" : [["F", "T'"]],
    "T'" : [["*", "F", "T'"], [parsers.EPSILON]],
    "F" : [["(", "E", ")"], ["int"]],
})

test_grammar2 = parsers.ContextFreeGrammar("A", {
    "A" : [["B", "D"]],
    "D" : [[lexer.Token(lexer.TokenType.OPERATOR, "+"), "B", "D"], [lexer.Token(lexer.TokenType.OPERATOR, "-"), "B", "D"], [parsers.EPSILON]],
    "B" : [["C", "B'"]],
    "B'" : [[lexer.Token(lexer.TokenType.OPERATOR, "*"), "B"], [lexer.Token(lexer.TokenType.OPERATOR, "/"), "B"], [parsers.EPSILON]],
    "C" : [[lexer.Token(lexer.TokenType.SEPARATOR, "("), "A", lexer.Token(lexer.TokenType.SEPARATOR, ")")], [lexer.Token(lexer.TokenType.INTEGER)]],
})


def compile_to_c(source):
    """Compiles funky source code.
    
    Input:
        source -- the source code for the program as a plain string.
        
    Returns:
        C source code, ready to be written to a file
    """

    symbol_table = {}

    # lexical analysis
    try:
        tokens = lexer.lex(source, lexer.regexes)
        print(tokens)
    except lexer.InvalidSourceException as e:
        err("Compilation failed during lexical analysis.")
        err("Error: \"{}\"".format(e.args[0]))
        exit(1)

    try:
        parser = parsers.llparser.LLParser(test_grammar2)
        parser.parse(tokens)
        print("String parsed successfully.")
    except parsers.ParsingError as e:
        err("Compilation failed during syntax analysis.")
        err("Error: \"{}\"".format(e.args[0]))
        exit(2)

    # TODO: syntax analysis
    pass

    # TODO: semantic analysis
    pass

    # TODO: intermediate code generation
    pass

    # TODO: optimisation
    pass

    # TODO: code generation
    pass

    # TODO: return finished product!
    pass
