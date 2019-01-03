"""Control flow for the compiler."""
import sys

from funky.exitcode import *

from funky.parser import FunkyLexingError, FunkySyntaxError, FunkySanityError, \
                         FunkyParsingError
from funky.parser.funky_parser import FunkyParser

from funky.util import err, get_user_attributes
import funky

def compile_to_c(source):
    """Compiles funky source code.
    
    Input:
        source -- the source code for the program as a plain string.
        
    Returns:
        C source code, ready to be written to a file
    """

    # lexical and syntax analysis
    try:
        parser = FunkyParser()
        parser.build()
        parsed = parser.do_parse(source)
    except FunkyLexingError as e:
        err("Failed to lex source code.")
        exit(LEXING_ERROR)
    except FunkySyntaxError as e:
        err("Syntax error in given program.")
        err("Error: \"{}\"".format(e.args[0]))
        exit(SYNTAX_ERROR)
    except FunkySanityError as e:
        err("Sanity checks for your source code failed.")
        err("Error: \"{}\"".format(e.args[0]))
        exit(SANITY_ERROR)
    except FunkyParsingError as e:
        err("Parsing error occurred during syntax analysis.")
        err("Error: \"{}\"".format(e.args[0]))
        exit(GENERIC_PARSING_ERROR)

    print("Parsing completed successfully.")

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
