"""REPL (read-evaluate-print-loop) for Funky."""

import argparse
import cmd
import copy
import logging
import os
import time
import traceback

from funky._version import __version__

import funky.globals
from funky.cli.verbosity import set_verbosity
from funky.util.color import *

from funky import FunkyError
from funky.parse import FunkyParsingError, FunkyLexingError, FunkySyntaxError
from funky.imports import FunkyImportError
from funky.rename import FunkyRenamingError
from funky.desugar import FunkyDesugarError
from funky.infer import FunkyTypeError
from funky.generate import FunkyCodeGenerationError

from funky.ds import Scope
from funky.corelang.coretree import *
from funky.corelang.builtins import TYPECLASSES

from funky.parse.funky_parser import FunkyParser
from funky.parse import fixity
from funky.imports.import_handler import get_imported_declarations
from funky.rename.rename import rename, check_scope_for_errors, MAIN
from funky.desugar.desugar import do_desugar, desugar, condense_function_binds, \
                                  split_typedefs_and_code
from funky.infer.infer import do_type_inference, infer

from funky.generate.gen_python_strict import StrictPythonCodeGenerator
from funky.generate.gen_python_lazy import LazyPythonCodeGenerator

log = logging.getLogger(__name__)

SHOW_EXCEPTION_TRACES = False

class CustomCmd(cmd.Cmd):
    """This is a 'hack' around Python's cmd.py builtin library. It appears that
    this module doesn't support a 'command prefix', which is what we want
    ideally for a REPL. What I mean by this is that there is no way to create a
    prefix, in our case ':', that specifies a command, with everything else
    just going to the default method.

    What I've done here is strip some code from the library and modify it to
    support this functionality. If this is flagged for plagiarism PLEASE READ
    THIS COMMENT!
    """

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.identchars += ":"

    def onecmd(self, line):
        """Interpret the argument as though it had been typed in response
        to the prompt.
        This may be overridden, but should not normally need to be;
        see the precmd() and postcmd() methods for useful execution hooks.
        The return value is a flag indicating whether interpretation of
        commands by the interpreter should stop.
        """
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line

        if line == 'EOF' :
            self.lastcmd = ''
            self.do_EOF(arg)
            return

        if cmd == '':
            return self.default(line)
        else:
            try:
                cmd = cmd[1:] # drop the ':'
                func = getattr(self, 'do_' + cmd)
            except AttributeError:
                return self.default(line)
            return func(arg)

    def parseline(self, line):
        """Parse the line into a command name and a string containing
        the arguments.  Returns a tuple containing (command, args, line).
        'command' and 'args' may be None if the line couldn't be parsed.
        """
        line = line.strip()
        if not line:
            return None, None, line
        elif line[0] == '?':
            line = 'help ' + line[1:]
        elif line[0] == '!':
            if hasattr(self, 'do_shell'):
                line = 'shell ' + line[1:]
            else:
                return None, None, line
        elif line[0] == ":":
            i, n = 0, len(line)
            while i < n and line[i] in self.identchars: i = i+1
            cmd, arg = line[:i], line[i:].strip()
            return cmd, arg, line
        elif line == "EOF":
            return "EOF", None, line
        else:
            return None, None, line

    def cmdloop(self, intro=None):
        # override the cmdloop function to handle ^C sensibly
        print(self.intro)
        while True:
            try:
                super().cmdloop(intro="")
                break
            except KeyboardInterrupt:
                print("^C")

def atomic(f):
    """This decorator is used in the FunkyShell class to mark a function as
    atomic. In this context, 'atomic' means that the operation either succeeds
    entirely or fails entirely. By marking do_* functions in the REPL as
    atomic, we ensure that if they fail, they do not leave the REPL in a broken
    state. For example, if an import fails, the state of the REPL is reverted
    to what it was before the user ever attempted the import.
    """
    def wrapper(self, *args, **kwargs):
        state = self.get_state()
        try:
            return f(self, *args, **kwargs)
        except FunkyError as e:
            self.revert_state(state)
            raise

    wrapper.__doc__ = f.__doc__
    return wrapper

def report_errors(f):
    """This decorator is used to wrap do_* functions in the command prompt
    below with error-catching and reporting code. Instead of having to repeat
    the same code for each function, we just tag each one where an error might
    occur with this decorator.
    """
    def wrapper(self, *args, **kwargs):
        err, e = None, None
        try:
            return f(self, *args, **kwargs)
        except FunkyParsingError as ex:
            e, err = ex, "Failed to parse"
        except FunkyImportError as ex:
            e, err = ex, "Import failure"
        except FunkyRenamingError as ex:
            e, err = ex, "Renaming error"
            self.scope.pending_definition = {}
        except FunkyDesugarError as ex:
            e, err = ex, "Desugarer error"
        except FunkyTypeError as ex:
            e, err = ex, "Code is not type-correct"
        except FunkyCodeGenerationError as ex:
            e, err = ex, "Code generation failed"
        except Exception as ex:
            e, err = ex, "Unexpected error"
            raise e

        err_msg = "{}: '{}'".format(err, str(e))
        print(cred(err_msg))
        if SHOW_EXCEPTION_TRACES:
            trace = "\n".join(traceback.format_tb(e.__traceback__))
            print(cred(trace))

    # ensure the wrapper function has the same docstring as the existing
    # function so that the help command still works!
    wrapper.__doc__ = f.__doc__
    return wrapper

class FunkyShell(CustomCmd):

    def __init__(self, lazy=False):
        start = time.time()
        super().__init__()

        self.intro   =  cgreen("\nfunkyi ({}) repl".format(__version__)) + \
                        "\nReady!\nFor help, use the ':help' command.\n"
        self.prompt  =  cyellow("funkyi> ")

        log.debug("Lazy mode {}.".format("enabled" if lazy else "disabled"))
        if lazy:
            print(cblue("Lazy evalation enabled."))
        else:
            print(cblue("Lazy evalation disabled."))

        # create the various parsers:
        log.debug("Creating required parsers...")
        self.decl_parser = FunkyParser()
        self.decl_parser.build(start="TOPLEVEL_DECLARATIONS")
        self.expr_parser = FunkyParser()
        self.expr_parser.build(start="EXP")
        self.newtype_parser = FunkyParser()
        self.newtype_parser.build(start="ADT_DECLARATION")
        self.setfix_parser = FunkyParser()
        self.setfix_parser.build(start="FIXITY_DECLARATION")
        self.import_parser = FunkyParser()
        self.import_parser.build(start="IMPORT_STATEMENT")

        if lazy:
            log.debug("Using lazy code generator for REPL.")
            self.py_generator = LazyPythonCodeGenerator()
        else:
            log.debug("Using strict code generator for REPL.")
            self.py_generator = StrictPythonCodeGenerator()

        log.debug("Done creating parsers.")

        self.reset()

        end = time.time()
        print(cblue("Startup completed ({0:.3f}s).".format(end - start)))

    @report_errors
    @atomic
    def do_begin_block(self, arg):
        """Start a block of definitions."""
        block_prompt = cyellow("block>  ")
        end_block = ":end_block" # <- type this to end the block
        lines = []
        try:
            while True:
                inp = input(block_prompt)
                if inp:
                    if inp == end_block:
                        break
                    lines.append(" " + inp)
        except KeyboardInterrupt:
            print("^C\n{}".format(cred("Cancelled block.")))
            return
        self.parse_and_add_declarations(lines)

    @report_errors
    @atomic
    def do_type(self, arg):
        """Show the type of an expression. E.g.: :type 5"""
        expr = self.get_core(arg)
        self.global_let.expr = expr
        do_type_inference(self.global_let, self.global_types)
        print("{} :: {}".format(arg, self.global_let.inferred_type))

    def do_lazy(self, arg):
        """Use ':lazy on' to use lazy evaluation and ':lazy off' to use strict evaluation."""
        SWAPPED = "Swapped to {} code generator.".format
        ALREADY = "Already using {} code generator; ignoring.".format
        if arg.lower() == "on":
            log.debug("Now using lazy code generator for REPL.")
            if isinstance(self.py_generator, StrictPythonCodeGenerator):
                self.py_generator = LazyPythonCodeGenerator()
                print(cgreen(SWAPPED("lazy")))
            else:
                print(ALREADY("lazy"))
        elif arg.lower() == "off":
            log.debug("Now using strict code generator for REPL.")
            if isinstance(self.py_generator, LazyPythonCodeGenerator):
                self.py_generator = StrictPythonCodeGenerator()
                print(cgreen(SWAPPED("strict")))
            else:
                print(ALREADY("strict"))
        else:
            print(cred("Invalid option '{}'. Please specify 'on' or "
                       "'off'.".format(arg)))

    def do_color(self, arg):
        """Use ':color on' to enable colors and ':color off' to disable them."""
        SWAPPED = "Turned colors {}.".format
        ALREADY = "Colors are already {}.".format
        
        if arg.lower() == "on":
            log.debug("Enabling colors.")
            if not funky.globals.USE_COLORS:
                funky.globals.USE_COLORS = True
                print(cgreen(SWAPPED("on")))
            else:
                print(ALREADY("on"))
        elif arg.lower() == "off":
            log.debug("Disabling colors.")
            if funky.globals.USE_COLORS:
                funky.globals.USE_COLORS = False
                print(cgreen(SWAPPED("off")))
            else:
                print(ALREADY("off"))
        else:
            print(cred("Invalid option '{}'. Please specify 'on' or "
                       "'off'.".format(arg)))

    def do_unicode(self, arg):
        """Use ':unicode on' to enable unicode characters and ':unicode off' to disable them."""
        SWAPPED = "Unicode printing is now {}.".format
        ALREADY = "Unicode printing is already {}.".format
        
        if arg.lower() == "on":
            log.debug("Enabling unicode printing.")
            if not funky.globals.USE_UNICODE:
                funky.globals.USE_UNICODE = True
                print(cgreen(SWAPPED("on")))
            else:
                print(ALREADY("on"))
        elif arg.lower() == "off":
            log.debug("Disabling unicode printing.")
            if funky.globals.USE_UNICODE:
                funky.globals.USE_UNICODE = False
                print(cgreen(SWAPPED("off")))
            else:
                print(ALREADY("off"))
        else:
            print(cred("Invalid option '{}'. Please specify 'on' or "
                       "'off'.".format(arg)))

    def do_list(self, arg):
        """List the current bindings in desuguared intermediate code."""
        if not (self.global_types or self.global_let.binds):
            print(cgreen("Nothing currently registered."))
            return

        print(cgreen("Currently registered bindings:"))
        if self.global_types:
            print("\n".join(str(b) for b in self.global_types))
        if self.global_let.binds:
            print("\n".join(str(b) for b in self.global_let.binds))

    def do_binds(self, arg):
        """List the available bindings."""
        if not self.scope.local:
            print("No bindings.")
            return

        print(cgreen("Available bindings:"))
        self.scope.pprint_local_binds()

    @report_errors
    @atomic
    def do_newtype(self, arg):
        """Create an ADT. E.g.: :newtype List = Cons Integer List | Nil"""
        parsed = self.newtype_parser.do_parse("newtype {}".format(arg))
        self.add_typedefs([parsed])

    @report_errors
    @atomic
    def do_show(self, arg):
        """Show the compiled code for an expression. E.g.: :show 1 + 1"""
        code = self.get_compiled(arg)
        print(code)

    @report_errors
    def do_setfix(self, arg):
        """Change the fixity of an operator. E.g.: :setfix leftassoc 8 **"""
        self.setfix_parser.do_parse("setfix {}".format(arg))

    @report_errors
    @atomic
    def do_import(self, arg):
        """Import a .fky file into the REPL. E.g.: :import "stdlib.fky"."""
        start = time.time()
        try:
            import_stmt = self.import_parser.do_parse("import {}".format(arg))

            cwd = os.path.abspath(os.getcwd())
            imports_source = get_imported_declarations(cwd, [import_stmt],
                                                       imported=self.imported)

            typedefs, code = split_typedefs_and_code(imports_source)

            self.add_typedefs(typedefs)
            self.add_declarations(code)

            end = time.time()
            print(cgreen("Successfully imported {0} ({1:.3f}s).".format(arg,
                                                                        end - start)))
        except FunkyError as e:
            # if an error occurs, extend the error message to tell the user
            # that the error occurred while importing *this* file.
            new_msg = "{} (while importing {})".format(e.args[0], arg)
            e.args = (new_msg,) + e.args[1:]
            raise

    def do_typeclass(self, arg):
        """Prints a quick summary of a typeclass."""
        try:
            typeclass = TYPECLASSES[arg]
            print(arg, typeclass.constraints_str())
        except KeyError:
            print(cred("Typeclass '{}' does not exist.".format(arg)))

    def do_reset(self, arg):
        """Reset the environment (clear the current list of bindings)."""
        self.reset()
        print(cgreen("All bindings reset."))

    def reset(self):
        """Resets the scope and bindings."""
        self.imported = set([])
        self.scope = Scope()

        # global_types is the collection of user-defined type declarations.
        self.global_types = []
        # global_let is a core let whose bindings are just the bindings the
        # user has introduced, and whose expression is 'dynamic' -- it is
        # changed each time the user asks for an expression to be evaluated and
        # recompiled as a new program to give the new result.
        self.global_let = CoreLet([], CoreLiteral(0))

    def get_state(self):
        return (
            copy.copy(self.imported),
            copy.deepcopy(self.scope),
            copy.deepcopy(self.global_types),
            copy.deepcopy(self.global_let)
        )

    def revert_state(self, state):
        self.imported, self.scope, self.global_types, self.global_let = state

    def get_core(self, source):
        """Converts a string of Funky code into the intermediate language.

        :param source: the source code to convert to the intermediate language
        :return:       the core code
        """
        parsed = self.expr_parser.do_parse(source)

        rename(parsed, self.scope)
        check_scope_for_errors(self.scope)
        core_tree, _ = do_desugar(parsed)
        return core_tree

    def get_compiled(self, source):
        """Converts a string of funky code into the target source language.

        :param source: the source code to convert to the target source language
        :return:       the compiled code in the target source language
        """
        core_expr = self.get_core(source)
        self.global_let.expr = core_expr
        do_type_inference(self.global_let, self.global_types)

        target_source = self.py_generator.do_generate_code(self.global_let,
                                                           self.global_types)
        return target_source

    def parse_and_add_declarations(self, lines):
        """Add a new block of declarations to global_let.

        :param lines: the Funky source code lines in the new block of
                      declarations
        """
        # shoehorn the lines into a 'fake' with clause so that they can be
        # parsed correctly.
        parsed = self.decl_parser.do_parse("func = 0 with\n{}".format(
                                        "\n".join(lines)))

        # extract the parsed declarations back out from our 'fake' with clause.
        declarations = parsed[0].expression.declarations

        self.add_declarations(declarations)

    def add_typedefs(self, typedefs):
        for typedef in typedefs:
            rename(typedef, self.scope)
            typedef = desugar(typedef)
            self.global_types.append(typedef)

    def add_declarations(self, declarations):
        self.global_let.expr = CoreLiteral(0)

        # rename and desugar each declaration one-by-one, and append each to
        # the (new_) global_let binds
        for decl in declarations:
            rename(decl, self.scope)
            core_tree, _ = do_desugar(decl)
            self.global_let.binds.append(core_tree)

        check_scope_for_errors(self.scope)
        self.global_let.binds = condense_function_binds(self.global_let.binds)
        self.global_let.create_dependency_graph()

        # type infer the new global let to check for inconsistencies
        do_type_inference(self.global_let, self.global_types)

    def do_EOF(self, line):
        """Exit safely."""
        print("^D\nEOF, exiting.")
        exit(0)

    @report_errors
    @atomic
    def default(self, arg):
        """This is called when the user does not type in any command in
        particular. Since this is a REPL, we should interpret the given
        text as an expression or a declaration
        """

        # if there are comments, drop them
        try:
            arg = arg[:arg.index("#")]
            if not arg:
                return
        except ValueError:
            pass

        try:
            # try treating as an expression...
            code = self.get_compiled(arg)
            print(cblue("= "), end="")
            try:
                exec(code, {"__name__" : "__main__"})
            except Exception as e:
                print(cred(str(e)))
        except FunkyParsingError:
            # if that didn't work, try treating as a declaration
            self.parse_and_add_declarations([arg])

    def emptyline(self):
        """Empty lines in the REPL do nothing."""
        pass

def main():
    funky.globals.CURRENT_MODE = funky.globals.Mode.REPL

    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action="version",
                        version='%(prog)s {version}'.format(version=__version__),
                        help="Output %(prog)s's version and quit.")
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help="Be verbose. You can stack this flag, i.e. -vvv.")
    parser.add_argument('-q', '--quiet', action='count', default=1,
                        help="Be quiet. You can stack this flag, i.e. -qqq.")
    parser.add_argument('-u', '--no-unicode', action='store_true',
                        help="Do not use unicode characters in output (for old "
                             "terminals).")
    parser.add_argument('-c', '--no-colors', action='store_true',
                        help="Do not use coloured output (for boring people).")
    parser.add_argument('-e', '--show-exception-traces', action='store_true',
                        default=False,
                        help="Show full exception traces.")
    parser.add_argument('-z', '--be-lazy', action='store_true',
                        default=False,
                        help="Generate lazy code where possible.")
    parser.add_argument("files", type=str,
                        nargs="*",
                        help="Load these programs into the REPL.")

    args = parser.parse_args()
    funky.globals.USE_UNICODE = not args.no_unicode
    funky.globals.USE_COLORS  = not args.no_colors

    verbosity = args.verbose - args.quiet
    set_verbosity(verbosity)

    global SHOW_EXCEPTION_TRACES
    SHOW_EXCEPTION_TRACES = args.show_exception_traces

    log.debug("Initialising REPL-shell...")
    shell = FunkyShell(lazy=args.be_lazy)
    for imp_file in args.files:
        shell.do_import("\"{}\"".format(imp_file)) # wrap in quotes to match import syntax
    log.debug("Done initialising REPL-shell...")

    log.debug("Entering REPL loop...")
    shell.cmdloop()

def start():
    """Exists only for setuptools."""
    main()

if __name__ == "__main__":
    main()
