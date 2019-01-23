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

from funky.intermediate import FunkyTypeError
from funky.intermediate.infer import do_type_inference

from funky.util import get_user_attributes
import funky

log = logging.getLogger(__name__)

def compile_to_c(source, dump_parsed=False,
                         dump_renamed=False,
                         dump_desugared=False,
                         dump_types=False):
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
            if dump_parsed:
                print("## DUMPED PARSE TREE")
                print(parsed)
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
            if dump_renamed:
                print("## DUMPED RENAMED PARSE TREE")
                print(parsed)
        except FunkyRenamingError as e:
            err_and_exit("Renaming your code failed.", e, RENAMING_ERROR)
        
        try:
            core_tree = do_desugar(parsed)
            if dump_desugared:
                print("## CORE (DESUGARED) CODE")
                print(core_tree)
        except FunkyDesugarError as e:
            err_and_exit("Desugaring failed.", e, DESUGAR_ERROR)
    except FunkyFrontendError:
        err_and_exit("Generic frontend error.", e, GENERIC_PARSING_ERROR)

    log.info("Parsing completed successfully.")

    try:
        try:
            types = do_type_inference(core_tree)
            if dump_types:
                print("## CORE TYPES")
                print(types)
        except FunkyTypeError as e:
            err_and_exit("Your program failed type checks, will not compile.",
                         e, TYPE_ERROR)
    except Exception as e:
        raise e
