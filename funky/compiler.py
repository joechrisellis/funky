"""Control flow for the compiler."""
import logging
import sys

from funky.exitcode import *

from funky.frontend import FunkyLexingError, FunkySyntaxError,    \
                           FunkyRenamingError, FunkyDesugarError, \
                           FunkyParsingError, FunkyFrontendError
from funky.frontend.funky_parser import FunkyParser
from funky.frontend.rename import do_rename
from funky.frontend.desugar import do_desugar
from funky.util import get_user_attributes
import funky

log = logging.getLogger(__name__)

def compile_to_c(source):
    """Compiles funky source code.
    
    Input:
        source -- the source code for the program as a plain string.
        
    Returns:
        C source code, ready to be written to a file
    """

    try: # frontend tasks
        # lex and parse code
        try:
            parser = FunkyParser()
            parser.build()
            parsed = parser.do_parse(source)
        except FunkyLexingError as e:
            err_and_exit("Failed to lex source code.", e, LEXING_ERROR)
        except FunkySyntaxError as e:
            err_and_exit("Syntax error in given program.", e, SYNTAX_ERROR)
        except FunkyParsingError as e:
            err_and_exit("Parsing error occurred during syntax analysis.", e,
                         GENERIC_PARSING_ERROR)

        # rename variables
        try:
            do_rename(parsed)
        except FunkyRenamingError as e:
            err_and_exit("Renaming your code failed.", e, RENAMING_ERROR)
        
        try:
            core_tree = do_desugar(parsed)
        except FunkyDesugarError as e:
            err_and_exit("Desugaring failed.", e, DESUGAR_ERROR)
    except FunkyFrontendError:
        err_and_exit("Generic frontend error.", e, GENERIC_PARSING_ERROR)

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
