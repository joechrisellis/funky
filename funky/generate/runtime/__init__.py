from funky.util.orderedset import OrderedSet
from funky.generate.gen import CodeSection

def add_to_runtime(f):
    def wrapper(self, *args, **kwargs):
        code, fname = f(self, *args, **kwargs)
        self.used_runtime_methods.add(code)
        return fname
    return wrapper

class Runtime:

    def __init__(self):
        # set of all runtime methods that are actually used. We keep track of
        # this so that we don't include unused methods.
        self.used_runtime_methods = OrderedSet()
        self.builtins = None

    def runtime_method(self, op):
        return self.builtins[op]()
    
    def get_runtime(self):
        runtime_section = CodeSection("runtime")
        for method_code in self.used_runtime_methods:
            runtime_section.emit(method_code)
            runtime_section.newline()
        return runtime_section
    
    def reset(self):
        self.used_runtime_methods.clear()
