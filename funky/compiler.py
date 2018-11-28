"""Control flow for the compiler."""
import sys

from funky.util import err
import funky.lexer as lexer
import funky.parsers as parsers
import funky.parsers.llparser as llparser

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
    except lexer.InvalidSourceException as e:
        err("Compilation failed during lexical analysis.")
        err("Error: \"{}\"".format(e.message))

    print(tokens)

    try:
        test_grammar = parsers.ContextFreeGrammar("E", {
            "E" : [["T", "E'"]],
            "E'" : [[lexer.Token(lexer.TokenType.OPERATOR, "+"), "T", "E'"], [parsers.EPSILON]],
            "T" : [["F", "T'"]],
            "T'" : [[lexer.Token(lexer.TokenType.OPERATOR, "*"), "F", "T'"], [parsers.EPSILON]],
            "F" : [[lexer.Token(lexer.TokenType.SEPARATOR, "("), "E", lexer.Token(lexer.TokenType.SEPARATOR, ")")], [lexer.Token(lexer.TokenType.INTEGER, None)]],
        })

        parser = parsers.llparser.LLParser(test_grammar)
        parser.parse(tokens)

    except parsers.ParsingError as e:
        err("Compilation failed during syntax analysis.")
        err("Error: \"{}\"".format(e.args[0]))
        pass

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
