import cmd
import copy

from funky._version import __version__
from funky.color import *

from funky.parse import FunkyParsingError, FunkyLexingError, FunkySyntaxError
from funky.rename import FunkyRenamingError
from funky.desugar import FunkyDesugarError
from funky.infer import FunkyTypeError

from funky.ds import Scope
from funky.corelang.coretree import *

from funky.parse.funky_parser import FunkyParser
from funky.parse import fixity
from funky.rename.rename import rename, check_scope_for_errors
from funky.desugar.desugar import do_desugar, desugar, condense_function_binds
from funky.infer.infer import do_type_inference, infer
from funky.generate.gen_python import PythonCodeGenerator

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

def report_errors(f):
    def wrapper(*args, **kwargs):
        err, e = None, None
        try:
            f(*args, **kwargs)
            return
        except FunkyParsingError as ex:
            e, err = ex, "Failed to parse"
        except FunkyRenamingError as ex:
            e, err = ex, "Renaming error"
        except FunkyDesugarError as ex:
            e, err = ex, "Desugarer error"
        except FunkyDesugarError as ex:
            e, err = ex, "Desugarer error"
        except FunkyTypeError as ex:
            e, err = ex, "Code is not type-correct"
        
        err_msg = "{}: '{}'".format(err, str(e))
        print(cred(err_msg))

    # ensure the wrapper function has the same docstring as the existing
    # function so that the :help command still works!
    wrapper.__doc__ = f.__doc__
    return wrapper

class FunkyShell(CustomCmd):

    intro   =  cgreen("funkyi ({}) repl".format(__version__))
    prompt  =  cyellow("funkyi> ")

    def __init__(self):
        super().__init__()
        self.decl_parser = FunkyParser()
        self.decl_parser.build(start="TOP_DECLARATIONS")
        self.expr_parser = FunkyParser()
        self.expr_parser.build(start="EXP")
        self.newcons_parser = FunkyParser()
        self.newcons_parser.build(start="NEW_CONS")
        self.setfix_parser = FunkyParser()
        self.setfix_parser.build(start="FIXITY_DECLARATION")
        self.scope = Scope()
        self.py_generator = PythonCodeGenerator()

        self.global_types = []
        self.global_let = CoreLet([], CoreLiteral(0))

    @report_errors
    def do_begin_block(self, arg):
        """Start a block of definitions."""
        block_prompt = cyellow("block > ")
        end_block = ":end_block"
        lines = []
        try:
            while True:
                inp = input(block_prompt)
                if inp == end_block:
                    break
                lines.append(" " + inp)
        except KeyboardInterrupt:
            print(cred("Cancelled block."))
            return
        self.add_declarations(lines)

    @report_errors
    def do_type(self, arg):
        """Show the type of an expression."""
        expr = self.get_core(arg)
        self.global_let.expr = expr
        do_type_inference(self.global_let, self.global_types)
        print("{} :: {}".format(arg, self.global_let.inferred_type))

    @report_errors
    def do_list(self, arg):
        """List the current bindings."""
        print("\n".join(str(b) for b in self.global_types))
        print("\n".join(str(b) for b in self.global_let.binds))
    
    @report_errors
    def do_newcons(self, arg):
        """Create an ADT."""
        stmt = self.newcons_parser.do_parse("newcons {}".format(arg))
        rename(stmt, self.scope)
        typedef = desugar(stmt)
        self.global_types.append(typedef)

    @report_errors
    def do_show(self, arg):
        code = self.get_compiled(arg)
        print(code)

    @report_errors
    def do_setfix(self, arg):
        self.setfix_parser.do_parse("setfix {}".format(arg))

    def get_core(self, code):
        try:
            parsed = self.expr_parser.do_parse(code)
        except FunkyParsingError:
            try:
                parsed = self.decl_parser.do_parse(code)[0]
            except FunkyParsingError:
                print("Cannot parse!")
                exit(1)

        rename(parsed, self.scope)
        check_scope_for_errors(self.scope)
        expr, _ = do_desugar(parsed)
        return expr

    def get_compiled(self, code):
        expr = self.get_core(code)
        self.global_let.expr = expr
        self.py_generator.reset()
        target_source = self.py_generator.do_generate_code(self.global_let,
                                                           self.global_types)
        return target_source

    def add_declarations(self, lines):
        new_global_let = copy.deepcopy(self.global_let)

        parsed = self.decl_parser.do_parse("func = 0 where\n{}".format(
                                        "\n".join(lines)))

        declarations = parsed[0].expression.declarations

        for decl in declarations:
            rename(decl, self.scope)
            core_tree, _ = do_desugar(decl)
            new_global_let.binds.append(core_tree)

        check_scope_for_errors(self.scope)

        new_global_let.binds = condense_function_binds(new_global_let.binds)

        do_type_inference(new_global_let, self.global_types)
        self.global_let = new_global_let

    def do_EOF(self, line):
        """Exit safely."""
        print("EOF, exiting.")
        exit(0)

    @report_errors
    def default(self, arg):
        # if there are comments, drop them
        try:
            arg = arg[:arg.index("#")]
            if not arg:
                return
        except ValueError:
            pass

        # try parsing as an expression...
        try:
            parsed = self.expr_parser.do_parse(arg)
            code = self.get_compiled(arg)
            print(cblue("= "), end="")
            exec(code, {"__name__" : "__main__"})
            return
        except FunkyParsingError:
            pass

        # if that didn't work, try parsing as a declaration
        try:
            parsed = self.decl_parser.do_parse(arg)[0]
            self.add_declarations([arg])
            return
        except FunkyParsingError:
            # if it can't be parsed as either, ignore the line
            # and report an error.
            print("Invalid syntax in supplied line.")

    def emptyline(self):
        pass

def main():
    try:
        shell = FunkyShell()
        shell.cmdloop()
    except KeyboardInterrupt:
        print("\nInterrupt caught, exiting.")
        exit(0)

def start():
    """Exists only for setuptools."""
    main()

if __name__ == "__main__":
    main()
