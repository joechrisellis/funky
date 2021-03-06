"""Control flow for the compiler."""
import logging
import os

from funky.util import get_registry_function
from funky.util.color import *

from funky.exitcode import *

import funky

from funky.parse import FunkyParsingError, FunkyLexingError, FunkySyntaxError
from funky.imports import FunkyImportError
from funky.rename import FunkyRenamingError
from funky.desugar import FunkyDesugarError
from funky.infer import FunkyTypeError
from funky.generate import FunkyCodeGenerationError

from funky.parse.funky_parser import FunkyParser
from funky.imports import libs_directory
from funky.imports.import_handler import get_imported_declarations
from funky.rename.rename import do_rename
from funky.desugar.desugar import do_desugar
from funky.infer.infer import do_type_inference

from funky.generate.gen_haskell import HaskellCodeGenerator
from funky.generate.gen_python_strict import StrictPythonCodeGenerator
from funky.generate.gen_python_lazy import LazyPythonCodeGenerator

log = logging.getLogger(__name__)

targets = {
    "haskell"       :  HaskellCodeGenerator,
    "python"        :  StrictPythonCodeGenerator,
    "python_lazy"   :  LazyPythonCodeGenerator,

    "intermediate"  :  None, # <-- handled by separate method!
}

def compiler_lex_and_parse(source, dump_pretty, dump_lexed, dump_parsed):
    """Lexes and parses the source code to get the syntax tree.
    
    :param source str:       the Funky source code
    :param dump_pretty bool: if true, dump the syntax-highlighted, prettified
                             code to stdout
    :param dump_lexed bool:  if true, dump the lexed code to stdout
    :param dump_parsed bool: if true, dump the syntax tree to stdout
    """
    # lex and parse code
    parser = FunkyParser()
    parser.build(dump_pretty=dump_pretty, dump_lexed=dump_lexed)
    # lexing is done in the same step as parsing -- so we have to tell the
    # parser whether we want the lexer's output to be displayed
    parsed = parser.do_parse(source)
    if dump_parsed:
        print(cblue("## DUMPED PARSE TREE"))
        print(parsed)
        print("")

    log.info("Parsing source code completed.")
    return parsed

def include_imports(filename, parsed, dump_imports):
    """Get the declarations from any imported source files and prepend
    them to the parse tree so that the declarations are made available in
    this file. Modifies the parse tree in place.
    
    :param filename str: the filename of the input file so that we can use
                         its dirname as a search path -- this allows us to
                         import files relative to the file the user is compiling
    :param parsed:       the parse tree
    """
    full_filename = os.path.abspath(filename)
    imports_source = get_imported_declarations(full_filename,
                                               parsed.body.imports)

    # weird syntax, but this is 'extending' from the start of the list.
    # we add the imported declarations to the start of the source file
    # we are compiling.
    parsed.body.toplevel_declarations[:0] = imports_source

    if dump_imports:
        print(cblue("## DUMPED PARSE TREE (with imports)"))
        print(parsed)
        print("")

def compiler_rename(parsed, dump_renamed):
    """Renames the syntax tree to avoid name shadowing and ensure that all
    items in the code are labelled uniquely. Modifies the syntax tree in
    place.
    
    :param parsed:            the syntax tree
    :param dump_renamed bool: if true, dump the renamed tree to stdout
    """
    # rename variables
    scope = do_rename(parsed)
    if dump_renamed:
        print(cblue("## DUMPED RENAMER MAPPING"))
        scope.pprint_local_binds()

        print("")
        print(cblue("## DUMPED RENAMED PARSE TREE"))
        print(parsed)
        print("")
    log.info("Renaming source code completed.")

def compiler_desugar(parsed, dump_desugared):
    """Desugars the renamed syntax tree to create the core tree.
    
    :param parsed:              the renamed syntax tree
    :param dump_desugared bool: if true, dump the core tree to stdout
    :return:                    the core tree
    """
    core_tree, typedefs = do_desugar(parsed)
    if dump_desugared:
        print(cblue("## TYPE DEFINITIONS"))
        print("\n".join(str(t) for t in typedefs))
        print(cblue("\n## CORE (DESUGARED) CODE"))
        print(core_tree)
        print("")
    
    log.info("Desugaring source code completed.")
    return core_tree, typedefs

def compiler_inference(core_tree, typedefs, dump_types):
    """Performs type inference on the core tree given a set of type
    definitions. Annotates the tree with types in place.
    
    :param core_tree:       the core tree (Funky intermediate language)
    :param typedefs:        the core type definitions
    :param dump_types bool: if true, dump the typed tree to stdout
    """
    do_type_inference(core_tree, typedefs)
    if dump_types:
        print(cblue("## ALGEBRAIC DATA TYPES"))
        for typedef in typedefs:
            print(typedef)

        print("")
        print(cblue("## TOPLEVEL TYPES"))
        for bind in core_tree.binds:
            print("{} :: {}".format(bind.identifier, bind.bindee.inferred_type))
        print("")

    log.info("Type inference completed.")

def compiler_generate(core_tree, typedefs, target, dump_generated):
    """Generate target code given the intermediate language code and type
    definitions.

    :param core_tree:           the core tree (Funky intermediate language)
    :param typedefs:            the core type definitions
    ;param target str:          the target language to compile to
    ;param dump_generated bool: if true, dump the generated code to stdout
    :return:                    the compiled target code as a string
    :rtype:                     str
    """
    target_generator = targets[target]()
    target_source = target_generator.do_generate_code(core_tree, typedefs)
    if dump_generated:
        print(cblue("## GENERATED {} CODE".format(target.upper())))
        print(target_source)
        print("")

    return target_source

def just_dump_desugared(core_tree, typedefs):
    """Instead of generating code, just return the desugared code in a serial
    format.
    """
    import pickle
    data = (core_tree, typedefs)
    return pickle.dumps(data)

def compile_file(infile, *args, **kwargs):
    """Given an input file, extracts the source code and compiles it. This is
    a wrapper function for compile_source below -- instead of taking the source
    as a string, it takes the source as a file. *args and **kwargs are passed
    to compile_source without modification.

    :param infile: the Funky source file to compile
    :return:       the target source code, ready to be written to a file
    """
    filename = infile.name
    lines = infile.readlines()
    log.info("Input file has {} lines.".format(len(lines)))
    source = "".join(lines)
    return compile_source(source, *args, filename=filename, **kwargs)

def compile_source(*args, **kwargs):
    """Compiles a Funky program, catching and reporting all errors as they
    occur. If an error occurs, we terminate. *args and **kwargs are passed to
    do_compile without modification.
    
    :return: the target source code, ready to be written to a file
    """
    try:
        return do_compile(*args, **kwargs)
    except FunkyLexingError as e:
        err_and_exit("Failed to lex source code.", e, LEXING_ERROR)
    except FunkySyntaxError as e:
        err_and_exit("Syntax error in given program.", e, SYNTAX_ERROR)
    except FunkyParsingError as e:
        err_and_exit("Parsing error occurred during syntax analysis.", e,
                     GENERIC_PARSING_ERROR)
    except FunkyRenamingError as e:
        err_and_exit("Renaming your code failed.", e, RENAMING_ERROR)
    except FunkyDesugarError as e:
        err_and_exit("Desugaring failed.", e, DESUGAR_ERROR)
    except FunkyTypeError as e:
        err_and_exit("Your program failed type checks, will not compile.",
                     e, TYPE_ERROR)
    except FunkyCodeGenerationError:
        err_and_exit("Code generation failed.", e, CODE_GENERATION_ERROR)

def do_compile(source, dump_pretty=False,
                       dump_lexed=False,
                       dump_parsed=False,
                       dump_imports=False,
                       dump_renamed=False,
                       dump_desugared=False,
                       dump_types=False,
                       dump_generated=False,
                       target=None,
                       filename=None):
    """Compiles funky source code.

    :param source str:          the source code for the program as a raw string
    :param dump_pretty bool:    dump the syntax-highlighted, prettified source
                                code to stdout.
    :param dump_lexed bool:     dump the output of the lexer to stdout
    :param dump_parsed bool:    dump the output of the parser to stdout
    :param dump_imports bool:   dump the output of the parser (with imports) to
                                stdout
    :param dump_renamed bool:   dump the output of the renamer to stdout
    :param dump_desugared bool: dump the output of the desugarer to stdout
    :param dump_types bool:     dump the output of the type checker to stdout
    :param dump_generated bool: dump the generated code to stdout
    :param target str:          the target to compile to
    :return:                    the target source code, ready to be written to
                                a file
    :rtype:                     str
    """
    parsed = compiler_lex_and_parse(source, dump_pretty, dump_lexed, dump_parsed)
    include_imports(filename, parsed, dump_imports)
    compiler_rename(parsed, dump_renamed)
    core_tree, typedefs = compiler_desugar(parsed, dump_desugared)
    compiler_inference(core_tree, typedefs, dump_types)

    if target == "intermediate":
        target_source = just_dump_desugared(core_tree, typedefs)
    else:
        target_source = compiler_generate(core_tree, typedefs, target,
                                          dump_generated)

    return target_source
