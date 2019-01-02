from funky.core.types import python_to_funky
from funky.util import get_user_attributes

class ASTNode:
    """Superclass for all abstract syntax tree nodes. Provides a __repr__
    function which allows the nodes to be printed nicely.
    """

    def __repr__(self):
        """Recursively outputs the node in the format:
            NodeName(attribute1=..., attribute2=...)
        """
        children = ", ".join("{}={}".format(a[0], repr(a[1]))
                             for a in get_user_attributes(self))
        return "{}({})".format(type(self).__name__, children)

class Module(ASTNode):
    """Node representing a module in Funky. Comprises a module ID and a program
    body.
    """

    def __init__(self, module_id, body):
        self.module_id  =  module_id
        self.body       =  body

class ProgramBody(ASTNode):
    """Node representing the body of a program -- this consists of zero or more
    import statements, followed by one or more top-level definitions.
    """

    def __init__(self, import_statements=[], toplevel_declarations=[]):
        self.import_statements      =  import_statements
        self.toplevel_declarations  =  toplevel_declarations

class ImportStatement(ASTNode):
    """Node representing an import statement -- an import statement includes
    the name of the module to import and (optionally) an alias.
    """

    def __init__(self, module_id):
        self.module_id  =  module_id

class NewTypeStatement(ASTNode):
    """Node representing a type alias. Consists of a new identifier and an
    'alias' -- the name of the old type. e.g.
        'newtype Currency = Float' becomes NewTypeStatement('Currency', 'Float')
    """

    def __init__(self, identifier, alias):
        self.identifier  =  identifier
        self.alias       =  alias

class TypeDeclaration(ASTNode):
    """Node representing a type declaration of some object. e.g.
        'f :: Integer -> Integer' becomes TypeDeclaration('f', ...)
    """

    def __init__(self, identifier, typ):
        self.identifier  =  identifier
        self.typ         =  typ

class Type(ASTNode):
    """A type -- e.g. Integer."""

    def __init__(self, type_name):
        self.type_name  =  type_name

class TupleType(ASTNode):
    """A tuple-type -- e.g. (Integer, Integer)."""

    def __init__(self, types):
        self.types  =  types
        self.arity  =  len(types)

class ListType(ASTNode):
    """A list-type --  e.g. [Integer]."""

    def __init__(self, typ):
        self.typ  =  typ

class FunctionType(ASTNode):
    """A function type -- e.g. [Integer] -> (Integer -> Integer) -> [Integer]"""

    def __init__(self, input_type, output_type=None):
        self.input_type   =  input_type
        self.output_type  =  output_type

class FunctionDefinition(ASTNode):
    """A function definition -- functions have a left hand side and a right
    hand side. The left hand side defines its identifier and its parameters,
    the right hand side defines its expression and any guards.
    """

    def __init__(self, lhs, rhs):
        self.lhs  =  lhs
        self.rhs  =  rhs

class FunctionLHS(ASTNode):
    """Function left-hand-sides consist of an identifier for the function and a
    list of parameters.
    """

    def __init__(self, identifier, parameters):
        self.identifier  =  identifier
        self.parameters  =  parameters

class FunctionRHS(ASTNode):
    """Function right-hand-sides consists of a list of possible expressions
    (some may be guarded!) and an optional set of 'where' declarations.
    """

    def __init__(self, expressions, declarations=[]):
        self.expressions   =  expressions
        self.declarations  =  declarations

class GuardedExpression(ASTNode):
    """A guarded expression is a feature of function right-hand-sides. It is an
    expression which should only be evaluated when one or more of its guard
    conditions are true. This node consists of a list of guard conditions which
    correspond to a particular expression.
    """

    def __init__(self, guard_conditions, expression):
        self.guard_conditions  =  guard_conditions
        self.expression        =  expression

class PatternDefinition(ASTNode):
    """Definition of a pattern -- i.e. pi = 3.14."""

    def __init__(self, pattern, expression):
        self.pattern     =  pattern
        self.expression  =  expression

class ConstructorChain(ASTNode):
    """A chain of list constructor calls. I.e. x : xs : []."""

    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

class Pattern(ASTNode):
    """A pattern."""

    def __init__(self, pat):
        self.pat  =  pat

class PatternTuple(ASTNode):
    """A tuple-pattern -- i.e. (a, b) or (_, _)."""

    def __init__(self, patterns):
        self.patterns = patterns

class PatternList(ASTNode):
    """A list pattern -- i.e. [x]."""

    def __init__(self, patterns):
        self.patterns  =  patterns

class Alternative(ASTNode):
    """In a match statement, an alternative is one possible pattern match."""

    def __init__(self, pattern, expression):
        self.pattern     =  pattern
        self.expression  =  expression

class Lambda(ASTNode):
    """A lambda declaration -- e.g. \\n -> n + 1. This will be boiled down to:
    """
    # TODO -- what does a multi-parameter lambda become?

    def __init__(self, parameters, expression):
        self.parameters  =  parameters
        self.expression  =  expression

class Let(ASTNode):
    """A let statement -- we can set identifiers to declarations only for a
    local scope.
    """

    def __init__(self, declarations, expression):
        self.declarations  =  declarations
        self.expression    =  expression

class If(ASTNode):
    """An if statement. If 'expression' evaluates to 'true', the 'then'
    expression is used. Otherwise, the 'otherwise' expression is used.
    """

    def __init__(self, expression, then, otherwise):
        self.expression  =  expression
        self.then        =  then
        self.otherwise   =  otherwise

class Match(ASTNode):
    """A match statement -- like a switch statement that can be used for
    pattern matching.
    """

    def __init__(self, expression, alternatives):
        self.expression    =  expression
        self.alternatives  =  alternatives

class FunctionApplication(ASTNode):
    """Application of a function to an expression. Note that the expression may
    be another function application, resulting in a function that returns a
    function (and allows for 'currying').
    """

    def __init__(self, func, expression):
        self.func        =  func
        self.expression  =  expression

class Tuple(ASTNode):
    """A tuple of expressions. E.g. (1, 2, 3)."""

    def __init__(self, items):
        self.items  =  items
        self.arity  =  len(items)

class List(ASTNode):
    """A list of expressions. E.g. [1, 2, 3]."""

    def __init__(self, items):
        self.items  =  items

class Literal(ASTNode):
    """Any literal value. Has a value and a type."""

    def __init__(self, value):
        self.value  =  value
        self.typ    =  python_to_funky[type(value)]

class InfixExpression(ASTNode):
    """An infix expression, e.g. 10 * 10. During parsing, we keep these FLAT --
    we perform fixity resolution later, whereby infix expressions become
    instances of FunctionApplications.
    """

    def __init__(self, tokens):
        self.tokens = tokens

class BinOpApplication(ASTNode):

    def __init__(self, operand1, operator, operand2):
        self.operand1 = operand1
        self.operator = operator
        self.operand2 = operand2

class UnaryOpApplication(ASTNode):

    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand
