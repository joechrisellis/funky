"""Control flow for the compiler."""
import sys

import lexer

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
        tokens = lexer.lex(source, lexer.regexes, symbol_table=symbol_table)
    except lexer.InvalidSourceException as e:
        print("Compilation failed during lexical analysis.", file=sys.stderr)
        print("Error: \"{}\"".format(e.message), file=sys.stderr)

    print(tokens)

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
