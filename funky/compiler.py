"""Control flow for the compiler."""
import logging
import sys

from funky.exitcode import *

from funky.util import get_registry_function
import funky

from funky.parse import FunkyParsingError, FunkyLexingError, FunkySyntaxError
from funky.rename import FunkyRenamingError
from funky.desugar import FunkyDesugarError
from funky.infer import FunkyTypeError
from funky.generate import FunkyCodeGenerationError

from funky.parse.funky_parser import FunkyParser
from funky.rename.rename import do_rename
from funky.desugar.desugar import do_desugar
from funky.infer.infer import do_type_inference
from funky.generate.gen_python import PythonCodeGenerator
from funky.generate.gen_c import CCodeGenerator

log = logging.getLogger(__name__)

targets = {
    "c"       :  CCodeGenerator,
    "python"  :  PythonCodeGenerator,
}

def compile_to_c(source, dump_lexed=False,
                         dump_parsed=False,
                         dump_renamed=False,
                         dump_desugared=False,
                         dump_types=False,
                         dump_generated=False,
                         target=None):
    """Compiles funky source code.

    :param source str: the source code for the program as a raw string.
    :return:           the C source code, ready to be written to a file.
    :rtype:            str
    """

    # lex and parse code
    try:
        parser = FunkyParser()
        parser.build()
        # lexing is done in the same step as parsing -- so we have to tell the
        # parser whether we want the lexer's output to be displayed
        parsed = parser.do_parse(source, dump_lexed=dump_lexed)
        if dump_parsed:
            print("## DUMPED PARSE TREE")
            print(parsed)
            print("")
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
            print("")
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
            print("")
    except FunkyDesugarError as e:
        err_and_exit("Desugaring failed.", e, DESUGAR_ERROR)

    log.info("Desugaring source code completed.")

    try:
        do_type_inference(core_tree, typedefs)
        if dump_types:
            print("## CORE TYPES")
            print(core_tree)
            print("")
    except FunkyTypeError as e:
        err_and_exit("Your program failed type checks, will not compile.",
                     e, TYPE_ERROR)

    log.info("Type inference completed.")

    try:
        target_generator = targets[target]()
        target_source = target_generator.do_generate_code(core_tree, typedefs)
        if dump_generated:
            print("## GENERATED {} CODE".format(target.upper()))
            print(target_source)
            print("")
    except FunkyCodeGenerationError:
        err_and_exit("Code generation failed.", e, CODE_GENERATION_ERROR)
