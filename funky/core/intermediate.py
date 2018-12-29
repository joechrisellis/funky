from funky.util import get_user_attributes

class ASTNode:

    def __repr__(self):
        children = ", ".join("{}={}".format(a[0], repr(a[1]))
                             for a in get_user_attributes(self))
        return "({}, {})".format(type(self).__name__, children)

class Module(ASTNode):

    def __init__(self, module_id, body):
        self.module_id  =  module_id
        self.body       =  body

class ProgramBody(ASTNode):
    
    def __init__(self, import_statements=[], toplevel_declarations=[]):
        self.import_statements      =  import_statements
        self.toplevel_declarations  =  toplevel_declarations

class ImportStatement(ASTNode):

    def __init__(self, module_id, alias=None):
        self.module_id  =  module_id
        self.alias      =  alias

class NewTypeStatement(ASTNode):

    def __init__(self, identifier, alias):
        self.identifier  =  identifier
        self.alias       =  alias

class TypeDeclaration(ASTNode):
    
    def __init__(self, identifier, typ):
        self.identifier  =  identifier
        self.typ         =  typ
