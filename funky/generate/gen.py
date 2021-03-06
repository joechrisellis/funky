from funky.generate import FunkyCodeGenerationError
from funky.corelang.types import contains_function
import datetime

class CodeGenerator:
    """A code generator. Code generators targeting a specific language should
    inherit from this base class.
    """

    def __init__(self, lang_name, comment):
        self.lang_name  =  lang_name
        self.comment    =  comment
        self.program    =  Program(self.lang_name, self.comment)

    def code_header(self):
        header_section = CodeSection()
        header_section.emit(self.comment("code generated by funky's {} "
                                         "generator".format(self.lang_name.lower())))
        header_section.emit(self.comment("timestamp: {}".format(self.timestamp())))
        header_section.newline()

        return header_section
    
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

        # if the type of the core tree is a function, we cannot output it.
        # technically, languages like Python can output a representation of it.
        # but languages like Haskell can't, so we should prevent it ever
        # happening for consistency.
        if contains_function(core_tree.inferred_type):
            raise FunkyCodeGenerationError("Output type contains a function. "
                                           "Cannot generate code which outputs "
                                           "function types.")

class Program:

    def __init__(self, lang_name, comment):
        self.lang_name  =  lang_name
        self.comment    =  comment
        self.reset()

    def get_code(self):
        code = ""
        for section in self.sections:
            if not section.code: continue
            if section.section_name:
                code += self.comment(section.section_name) + "\n"
            code += section.code
        return code

    def add_section(self, section, pos=0):
        self.sections.insert(pos, section)
    
    def reset(self):
        """Resets the state of the code generator so it can be used again."""
        self.sections  =  []

class CodeSection:

    def __init__(self, section_name=None):
        self.code          =  ""
        self.section_name  =  section_name

    def emit(self, s, d=0):
        """Emit a string to the program buffer.
        
        :param s str:      the string to emit
        :param d int:      how many spaces of indentation to apply (default: 0)
        """
        self.code += "{}{}\n".format(" " * d, s)

    def newline(self):
        """Emit a newline to the program buffer."""
        self.emit("")
