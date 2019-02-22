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

from funky.generate.gen_c import CCodeGenerator
from funky.generate.gen_haskell import HaskellCodeGenerator
from funky.generate.gen_python import PythonCodeGenerator

log = logging.getLogger(__name__)

targets = {
    "c"        :  CCodeGenerator,
    "haskell"  :  HaskellCodeGenerator,
    "python"   :  PythonCodeGenerator,
}

def compiler_parse_and_lex(source, dump_lexed, dump_parsed):
    # lex and parse code
    try:
        parser = FunkyParser()
        parser.build(dump_lexed=dump_lexed)
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

    return parsed

def compiler_rename(parsed, dump_renamed):
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

def compiler_desugar(parsed, dump_desugared):
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
    return core_tree, typedefs

def compiler_inference(core_tree, typedefs, dump_types):
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

def compiler_generate(core_tree, typedefs, target, dump_generated):
    try:
        target_generator = targets[target]()
        target_source = target_generator.do_generate_code(core_tree, typedefs)
        if dump_generated:
            print("## GENERATED {} CODE".format(target.upper()))
            print(target_source)
            print("")
    except FunkyCodeGenerationError:
        err_and_exit("Code generation failed.", e, CODE_GENERATION_ERROR)

    return target_source

def compile(source, dump_lexed=False,
                    dump_parsed=False,
                    dump_renamed=False,
                    dump_desugared=False,
                    dump_types=False,
                    dump_generated=False,
                    target=None):
    """Compiles funky source code.

    :param source str:          the source code for the program as a raw string
    :param dump_lexed bool:     dump the output of the lexer to stdout
    :param dump_parsed bool:    dump the output of the parser to stdout
    :param dump_renamed bool:   dump the output of the renamer to stdout
    :param dump_desugared bool: dump the output of the desugarer to stdout
    :param dump_types bool:     dump the output of the type checker to stdout
    :param dump_generated bool: dump the generated code to stdout
    :param target str:          the target to compile to
    :return:                    the target source code, ready to be written to
                                a file
    :rtype:                     str
    """

    parsed = compiler_parse_and_lex(source, dump_lexed, dump_parsed)
    compiler_rename(parsed, dump_renamed)
    core_tree, typedefs = compiler_desugar(parsed, dump_desugared)
    compiler_inference(core_tree, typedefs, dump_types)
    target_source = compiler_generate(core_tree, typedefs, target, dump_generated)

    return target_source
