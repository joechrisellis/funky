import cmd

from funky._version import __version__

from funky.parse import FunkyParsingError, FunkyLexingError, FunkySyntaxError
from funky.rename import FunkyRenamingError
from funky.desugar import FunkyDesugarError

from funky.parse.funky_parser import FunkyParser
from funky.rename.rename import do_rename
from funky.desugar.desugar import do_desugar

class FunkyShell(cmd.Cmd):

    intro   =  "funky ({})  shell".format(__version__)
    prompt  =  "funky> "

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.parser = FunkyParser()
        self.parser.build(start="TOP_DECLARATIONS", dump_lexed=True)

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
    
    def run_lines(self, lines):
        parsed = self.parser.do_parse("func = 0 where\n{}".format(
                                        "\n".join(lines)))
        declarations = parsed[0].expression.declarations
        print(declarations)

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
