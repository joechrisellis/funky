"""Control flow for the compiler."""
import sys

from funky.util import err
import funky
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
        print(tokens)
    except lexer.InvalidSourceException as e:
        err("Compilation failed during lexical analysis.")
        err("Error: \"{}\"".format(e.args[0]))
        exit(1)

    try:
        parser = parsers.llparser.LLParser(funky.FUNKY_GRAMMAR)
        ast = parser.parse(tokens)
        print("Source parsed successfully.")
        print(ast)
    except parsers.ParsingError as e:
        err("Compilation failed during syntax analysis.")
        err("Error: \"{}\"".format(e.args[0]))
        exit(2)

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
