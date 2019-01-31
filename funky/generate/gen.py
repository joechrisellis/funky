import datetime

def annotate_section(f):
    def wrapper(*args, **kwargs):
        self = args[0]
        self.comment("section: {}".format(f.__name__))
        f(*args, **kwargs)
        self.newline()
    return wrapper

class CodeGenerator:

    def __init__(self):
        self.program = ""

    def emit(self, s, d=0):
        self.program += "{}{}\n".format(" " * d, s)

    def newline(self):
        self.program += "\n"

    def timestamp(self):
        s = datetime.datetime.today().strftime('%Y-%m-%d at %H:%M:%S')
        self.comment(s)

    def comment(self, string):
        raise NotImplementedError("Comments not defined for this target.")

    def do_generate_code(self, core_tree, typedefs):
        raise NotImplementedError("Code generation not defined for this target.")
