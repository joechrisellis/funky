from funky.util import get_user_attributes

class ASTNode:

    def __repr__(self):
        children = ", ".join("{}={}".format(a[0], repr(a[1]))
                             for a in get_user_attributes(self))
        return "{}({})".format(type(self).__name__, children)

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

class Type(ASTNode):

    def __init__(self, type_name):
        self.type_name  =  type_name

class TupleType(ASTNode):

    def __init__(self, types):
        self.types  =  types
        self.arity  =  len(types)

class ListType(ASTNode):

    def __init__(self, typ):
        self.typ  =  typ

class FunctionType(ASTNode):

    def __init__(self, input_type, output_type=None):
        self.input_type   =  input_type
        self.output_type  =  output_type

class FunctionDefinition(ASTNode):

    def __init__(self, lhs, rhs):
        self.lhs  =  lhs
        self.rhs  =  rhs

class FunctionLHS(ASTNode):

    def __init__(self, identifier, parameters):
        self.identifier  =  identifier
        self.parameters  =  parameters

class FunctionRHS(ASTNode):

    def __init__(self, guarded_expressions, declarations=[]):
        self.guarded_expressions  =  guarded_expressions
        self.declarations         =  declarations

class GuardedExpression(ASTNode):

    def __init__(self, guard_conditions, expression):
        self.guard_conditions  =  guard_conditions
        self.expression        =  expression

class PatternDefinition(ASTNode):

    def __init__(self, pattern, expression):
        self.pattern     =  pattern
        self.expression  =  expression

class ConstructorChain(ASTNode):

    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

class Pattern(ASTNode):

    def __init__(self, pat):
        self.pat  =  pat

class PatternTuple(ASTNode):

    def __init__(self, patterns):
        self.patterns = patterns

class PatternList(ASTNode):

    def __init__(self, patterns):
        self.patterns  =  patterns

class Alternative(ASTNode):
    
    def __init__(self, pattern, expression):
        self.pattern     =  pattern
        self.expression  =  expression

class InfixExpression(ASTNode):
    
    def __init__(self, op):
        pass

class Lambda(ASTNode):
    
    def __init__(self, parameters, expression):
        self.parameters  =  parameters
        self.expression  =  expression

class Let(ASTNode):

    def __init__(self, declarations, expression):
        self.declarations  =  declarations
        self.expression    =  expression

class If(ASTNode):

    def __init__(self, expression, then, otherwise):
        self.expression  =  expression
        self.then        =  then
        self.otherwise   =  otherwise

class Match(ASTNode):

    def __init__(self, expression, alternatives):
        self.expression    =  expression
        self.alternatives  =  alternatives

class FunctionApplication(ASTNode):

    def __init__(self, func, expression):
        self.func        =  func
        self.expression  =  expression

class Tuple(ASTNode):

    def __init__(self, items):
        self.items  =  items
        self.arity  =  len(items)

class List(ASTNode):
    
    def __init__(self, items):
        self.items  =  items

class Literal(ASTNode):

    def __init__(self, value):
        self.value  =  value

class BinaryOperator(ASTNode):
    
    def __init__(self, left_operand, right_operand):
        self.left_operand   =  left_operand
        self.right_operand  =  left_operand
