"""Control flow for the compiler."""
import sys

from funky.parser.funky_parser import FunkyParser
from funky.parser import FunkyParsingError, FunkySyntaxError
from funky.util import err
import funky

def compile_to_c(source):
    """Compiles funky source code.
    
    Input:
        source -- the source code for the program as a plain string.
        
    Returns:
        C source code, ready to be written to a file
    """

    symbol_table = {}

    # lexical and syntax analysis
    try:
        parser = FunkyParser()
        parser.build()
        parsed = parser.do_parse(source)
    except FunkySyntaxError as e:
        err("Syntax error in given program.")
        err("Error: \"{}\"".format(e.args[0]))
        exit(2)
    except FunkyParsingError as e:
        err("Compilation failed during syntax analysis.")
        err("Error: \"{}\"".format(e.args[0]))
        exit(3)

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
