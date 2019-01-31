import datetime

def annotate_section(f):
    """Use this decorator on a function if you want to emit an annotation
    detailing the start of a section in the source code. For example, if you
    apply this decorator to a function `header`, the code generator will
    print 'section: header' as a comment before any emitted code from that
    section.
    """
    def wrapper(*args, **kwargs):
        self = args[0]
        self.comment("section: {}".format(f.__name__))
        f(*args, **kwargs)
        self.newline()
    return wrapper

class CodeGenerator:
    """A code generator. Maintains an internal 'program' buffer that will
    contain the source of the target language. Provides helper functions to
    'emit' code to this buffer. Code generators targeting a specific language
    should inherit from this base class.
    """

    def __init__(self):
        self.program = ""

    def emit(self, s, d=0):
        """Emit a string to the program buffer.
        
        :param s str: the string to emit
        :param d int: how many spaces of indentation to apply (default: 0)
        """
        self.program += "{}{}\n".format(" " * d, s)

    def newline(self):
        """Emit a newline to the program buffer."""
        self.emit("")

    def timestamp(self):
        """Get the current time as a string. This can then be emitted to the
        generated code to 'timestamp' compiler artifacts.
        """
        return datetime.datetime.today().strftime('%Y-%m-%d at %H:%M:%S')

    def do_generate_code(self, core_tree, typedefs):
        """Generate code for this target.
        
        :param core_tree CoreNode:            the core tree to compile
        :param typedefs [CoreTypeDefinition]: a list of type definitions
        """
        raise NotImplementedError("Code generation not defined for this target.")
