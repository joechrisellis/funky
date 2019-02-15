import cmd
import copy

from funky._version import __version__

from funky.parse import FunkyParsingError, FunkyLexingError, FunkySyntaxError
from funky.rename import FunkyRenamingError
from funky.desugar import FunkyDesugarError
from funky.infer import FunkyTypeError

from funky.ds import Scope
from funky.corelang.coretree import *

from funky.parse.funky_parser import FunkyParser
from funky.rename.rename import rename
from funky.desugar.desugar import do_desugar, condense_function_binds
from funky.infer.infer import do_type_inference, infer
from funky.generate.gen_python import PythonCodeGenerator

class CustomCmd(cmd.Cmd):

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
        else:
            return None, None, line

class FunkyShell(CustomCmd):

    intro   =  "funky ({}) shell".format(__version__)
    prompt  =  "funky> "

    def __init__(self):
        super().__init__()
        self.decl_parser = FunkyParser()
        self.decl_parser.build(start="TOP_DECLARATIONS")
        self.expr_parser = FunkyParser()
        self.expr_parser.build(start="EXP")
        self.scope = Scope()
        self.py_generator = PythonCodeGenerator()

        self.global_let = CoreLet([], CoreLiteral(0))

    def do_begin_block(self, arg):
        """Start a block of definitions."""
        block_prompt = "block> "
        end_block = ":end_block"
        lines = []
        while True:
            inp = input(block_prompt)
            if inp == end_block:
                break
            lines.append(" " + inp)
        self.run_lines(lines)

    def do_type(self, arg):
        """Show the type of an expression."""
        expr, typedefs = self.get_core(arg)
        self.global_let.expr = expr
        try:
            do_type_inference(self.global_let, typedefs)
            print("{} :: {}".format(arg, self.global_let.inferred_type))
        except FunkyTypeError:
            print("Expression is not type correct.")

    def do_list(self, arg):
        """List the current bindings."""
        print("\n".join(str(b) for b in self.global_let.binds))

    def do_let(self, arg):
        """Bind a name on a single line."""
        self.run_lines([arg])

    def do_show(self, arg):
        code = self.get_compiled(arg)
        print(code)

    def get_core(self, code):
        parsed = self.expr_parser.do_parse(code)
        rename(parsed, self.scope)
        expr, typedefs = do_desugar(parsed)
        return expr, typedefs

    def get_compiled(self, code):
        expr, typedefs = self.get_core(code)

        self.global_let.expr = expr
        self.py_generator.reset()
        target_source = self.py_generator.do_generate_code(self.global_let, [])
        return target_source

    def run_lines(self, lines):
        old_global_let = copy.deepcopy(self.global_let)

        parsed = self.decl_parser.do_parse("func = 0 where\n{}".format(
                                        "\n".join(lines)))

        declarations = parsed[0].expression.declarations
        for decl in declarations:
            rename(decl, self.scope)
            core_tree, typedefs = do_desugar(decl)
            self.global_let.binds.append(core_tree)

        self.global_let.binds = condense_function_binds(self.global_let.binds)

        try:
            do_type_inference(self.global_let, typedefs)
        except FunkyTypeError as e:
            print("Code is not type-correct.")
            print(str(e))
            print("Ignoring.")
            self.global_let = old_global_let

    def do_EOF(self, line):
        """Exit safely."""
        print("EOF, exiting.")
        exit(0)

    def default(self, arg):
        code = self.get_compiled(arg)
        exec(code, {"__name__" : "__main__"})

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
