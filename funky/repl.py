import cmd

from funky._version import __version__

from funky.parse import FunkyParsingError, FunkyLexingError, FunkySyntaxError
from funky.rename import FunkyRenamingError
from funky.desugar import FunkyDesugarError

from funky.ds import Scope
from funky.corelang.coretree import *

from funky.parse.funky_parser import FunkyParser
from funky.rename.rename import rename
from funky.desugar.desugar import desugar

class FunkyShell(cmd.Cmd):

    intro   =  "funky ({}) shell".format(__version__)
    prompt  =  "funky> "

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.decl_parser = FunkyParser()
        self.decl_parser.build(start="TOP_DECLARATIONS")
        self.expr_parser = FunkyParser()
        self.expr_parser.build(start="EXP")
        self.scope = Scope()
        self.binds = []

    def do_begin_block(self, arg):
        """Start a block of definitions."""
        block_prompt = "block> "
        lines = []
        while True:
            inp = input(block_prompt)
            if inp == "end_block":
                break
            lines.append(" " + inp)
        self.run_lines(lines)

    def do_let(self, arg):
        """Bind a name on a single line."""
        self.run_lines([arg])

    def do_exec(self, arg):
        parsed = self.expr_parser.do_parse(arg)
        rename(parsed, self.scope)
        expr = desugar(parsed)

        print(CoreLet(self.binds, expr))

    def run_lines(self, lines):
        parsed = self.decl_parser.do_parse("func = 0 where\n{}".format(
                                        "\n".join(lines)))

        declarations = parsed[0].expression.declarations
        for decl in declarations:
            rename(decl, self.scope)
            self.binds.append(desugar(decl))
        do_type_inference(core_tree, typedefs)

    def do_EOF(self, line):
        """Exit safely."""
        print("EOF, exiting.")
        exit(0)

def main():
    FunkyShell().cmdloop()

def start():
    """Exists only for setuptools."""
    main()

if __name__ == "__main__":
    main()
