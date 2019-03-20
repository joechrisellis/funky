from io import StringIO
import contextlib
import sys

from funky.cli.verbosity import set_loglevel
import funky.compiler as compiler

@contextlib.contextmanager
def stdoutIO(stdout=None):
    """Context manager to capture stdout."""
    old = sys.stdout
    if stdout is None: stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

class FunkyCallable:

    def __init__(self, py_code):
        self.py_code = py_code

    def __call__(self):
        with stdoutIO() as s:
            exec(self.py_code, {"__name__" : "__main__"})
        return s.getvalue().strip()

def funky_prog(source, lazy=False):
    target = "python_lazy" if lazy else "python"
    py_code = compiler.do_compile(source, filename=".", target=target)
    return FunkyCallable(py_code)

prog = funky_prog("""
module test with
    
    import "lists.fky"
    
    main = nth 20 fibs
""", lazy=True)
x = prog()
print(x)
