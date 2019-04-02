"""Python foreign function interface for Funky. Allows a programmer to embed
Funky code in a Python program, compile it, and run it.

To use:
from funky.ffi import funky_prog # <- in your Python program
prog = funky_prog(<FUNKY CODE AS A STRING>)
x = prog() # <- compile and run
"""

import logging

import funky.cli.verbosity as verbosity
import funky.compiler as compiler

class FunkyCallable:
    """Container for a Funky program compiled to Python code. When called, this
    object will run the Python code and return its result. We call the 'result'
    function within the compiled program, which returns the *raw data* used
    internally in Funky (not guaranteed to be any specific representation, like
    a string!). In other words, if the result of the main method in the given
    Funky program is an ADT, this callable will return the ADT in Funks's
    internal representation.
    """

    def __init__(self, py_code):
        self.py_code = py_code
        self.memo    = None

    def __call__(self):
        """Check if we have a memo -- if we do, this has already been run, so
        just return the cached result. If we don't, compute it and save the
        memo.
        """
        if self.memo:
            return self.memo
        g = {}
        exec(self.py_code, g)
        self.memo = g["result"]()
        return self.memo

def funky_prog(source, lazy=False, verbosity_value=verbosity.quietest):
    """Creates a FunkyCallable object whose code is the result of compiling the
    given source code. If lazy is True, we use the lazy Python code generator.
    If lazy is False, we use the strict Python code generator.
    
    The result of this function can be called (as if it were a function!), which
    will then return the result of executing the Funky code.
    
    :param source: the Funky source code to compile
    :param lazy:   whether or not to use the lazy Python code generator
    :return:       a FunkyCallable object that, when called, will compile the
                   Funky source into Python, run it, and return the result
    """
    target = "python_lazy" if lazy else "python"

    old_loglevel = logging.getLogger().getEffectiveLevel()
    verbosity.set_verbosity(verbosity_value)
    py_code = compiler.do_compile(source, filename=".", target=target)

    logging.getLogger().setLevel(old_loglevel)
    return FunkyCallable(py_code)
