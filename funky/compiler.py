"""Control flow for the compiler."""
import logging
import sys

from funky.exitcode import *

from funky.util import get_user_attributes
import funky

from funky.parse import FunkyParsingError, FunkyLexingError, FunkySyntaxError
from funky.parse.funky_parser import FunkyParser

from funky.rename.rename import do_rename

from funky.desugar.desugar import do_desugar

from funky.infer import FunkyTypeError
from funky.infer.infer import do_type_inference

log = logging.getLogger(__name__)

def compile_to_c(source, dump_parsed=False,
                         dump_renamed=False,
                         dump_desugared=False,
                         dump_types=False):
    """Compiles funky source code.

    :param source str: the source code for the program as a raw string.
    :return:           the C source code, ready to be written to a file.
    :rtype:            str
    """

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

    log.info("Parsing source code completed.")

    # rename variables
    try:
        do_rename(parsed)
        if dump_renamed:
            print("## DUMPED RENAMED PARSE TREE")
            print(parsed)
    except FunkyRenamingError as e:
        err_and_exit("Renaming your code failed.", e, RENAMING_ERROR)

    log.info("Renaming source code completed.")
    
    try:
        core_tree, typedefs = do_desugar(parsed)
        if dump_desugared:
            print("## TYPE DEFINITIONS")
            print("\n".join(str(t) for t in typedefs))
            print("\n## CORE (DESUGARED) CODE")
            print(core_tree)
    except FunkyDesugarError as e:
        err_and_exit("Desugaring failed.", e, DESUGAR_ERROR)

    log.info("Desugaring source code completed.")

    try:
        types = do_type_inference(core_tree, typedefs)
        if dump_types:
            print("## CORE TYPES")
            print(types)
    except FunkyTypeError as e:
        err_and_exit("Your program failed type checks, will not compile.",
                     e, TYPE_ERROR)

    log.info("Type inference completed.")
