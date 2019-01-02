from funky.core.types import python_to_funky, primitives
from funky.parser import FunkySanityError
from funky.util import get_user_attributes

class ASTNode:
    """Superclass for all abstract syntax tree nodes. Provides a __repr__
    function which allows the nodes to be printed nicely.
    """

    def sanity_check(self, scope):
        raise NotImplementedError

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

    def sanity_check(self, scope=[]):
        scope = self.body.sanity_check(scope)
        return scope

class ProgramBody(ASTNode):
    """Node representing the body of a program -- this consists of zero or more
    import statements, followed by one or more top-level definitions.
    """

    def __init__(self, import_statements=[], toplevel_declarations=[]):
        self.import_statements      =  import_statements
        self.toplevel_declarations  =  toplevel_declarations

    def sanity_check(self, scope):
        for decl in self.import_statements:
            scope = decl.sanity_check(scope)

        for decl in self.toplevel_declarations:
            scope = decl.sanity_check(scope)

        return scope

class ImportStatement(ASTNode):
    """Node representing an import statement -- an import statement includes
    the name of the module to import and (optionally) an alias.
    """

    def __init__(self, module_id):
        self.module_id  =  module_id

    def sanity_check(self, scope):
        # TODO: import all variables from the module into the scope
        return scope

class NewTypeStatement(ASTNode):
    """Node representing a type alias. Consists of a new identifier and an
    'alias' -- the name of the old type. e.g.
        'newtype Currency = Float' becomes NewTypeStatement('Currency', 'Float')
    """

    def __init__(self, identifier, typ):
        self.identifier  =  identifier
        self.typ         =  typ

    def sanity_check(self, scope):
        if self.identifier in scope:
            raise FunkySanityError("Duplicate type '{}'.".format(self.identifier))
        self.typ.sanity_check(scope)
        scope = scope + [self.identifier]
        return scope

class TypeDeclaration(ASTNode):
    """Node representing a type declaration of some object. e.g.
        'f :: Integer -> Integer' becomes TypeDeclaration('f', ...)
    """

    def __init__(self, identifier, typ):
        self.identifier  =  identifier
        self.typ         =  typ

    def sanity_check(self, scope):
        scope = self.typ.sanity_check(scope)

        # We do not add the identifier to the scope -- simply defining the type
        # of a variable is not enough to say that it can be used. We handle this
        # further in type checking.
        return scope

class Type(ASTNode):
    """A type -- e.g. Integer."""

    def __init__(self, type_name):
        self.type_name  =  type_name

    def sanity_check(self, scope):
        if self.type_name not in scope and self.type_name not in primitives:
            raise FunkySanityError("Undefined type '{}'.".format(self.type_name))
        return scope

class TupleType(ASTNode):
    """A tuple-type -- e.g. (Integer, Integer)."""

    def __init__(self, types):
        self.types  =  types
        self.arity  =  len(types)

    def sanity_check(self, scope):
        for typ in self.types:
            scope = typ.sanity_check(scope)
        return scope

class ListType(ASTNode):
    """A list-type --  e.g. [Integer]."""

    def __init__(self, typ):
        self.typ  =  typ

    def sanity_check(self, scope):
        scope = self.typ.sanity_check(scope)
        return scope

class FunctionType(ASTNode):
    """A function type -- e.g. [Integer] -> (Integer -> Integer) -> [Integer]"""

    def __init__(self, input_type, output_type=None):
        self.input_type   =  input_type
        self.output_type  =  output_type

    def sanity_check(self, scope):
        scope = self.input_type.sanity_check(scope)
        scope = self.output_type.sanity_check(scope)
        return scope

class FunctionDefinition(ASTNode):
    """A function definition -- functions have a left hand side and a right
    hand side. The left hand side defines its identifier and its parameters,
    the right hand side defines its expression and any guards.
    """

    def __init__(self, lhs, rhs):
        self.lhs  =  lhs
        self.rhs  =  rhs

    def sanity_check(self, scope):
        func_scope = self.lhs.sanity_check(scope)
        func_scope = self.rhs.sanity_check(func_scope)

        scope = scope + [self.lhs.identifier]
        return scope

class FunctionLHS(ASTNode):
    """Function left-hand-sides consist of an identifier for the function and a
    list of parameters.
    """

    def __init__(self, identifier, parameters):
        self.identifier  =  identifier
        self.parameters  =  parameters

    def sanity_check(self, scope):
        if self.identifier in scope:
            raise FunkySanityError("Duplicate definition of " \
                                   "'{}'.".format(self.identifier))

        scope = scope + [self.identifier]
        for param in self.parameters:
            scope = param.sanity_check(scope)

        return scope

class FunctionRHS(ASTNode):
    """Function right-hand-sides consists of a list of possible expressions
    (some may be guarded!) and an optional set of 'where' declarations.
    """

    def __init__(self, expressions, declarations=[]):
        self.expressions   =  expressions
        self.declarations  =  declarations

    def sanity_check(self, scope):
        # update the scope to include variables defined in a where
        # clause. TODO: won't allow the same variable to be redefined in a
        # more local scope!!
        for decl in self.declarations:
            scope = scope + decl.sanity_check(scope)

        for exp in self.expressions:
            scope = exp.sanity_check(scope)

        return scope

class GuardedExpression(ASTNode):
    """A guarded expression is a feature of function right-hand-sides. It is an
    expression which should only be evaluated when one or more of its guard
    conditions are true. This node consists of a list of guard conditions which
    correspond to a particular expression.
    """

    def __init__(self, guard_conditions, expression):
        self.guard_conditions  =  guard_conditions
        self.expression        =  expression

    def sanity_check(self, scope):
        for cond in self.guard_conditions:
            scope = cond.sanity_check(scope)

        scope = self.expression.sanity_check(scope)
        return scope

class PatternDefinition(ASTNode):
    """Definition of a pattern -- i.e. pi = 3.14."""

    def __init__(self, pattern, expression):
        self.pattern     =  pattern
        self.expression  =  expression

    def sanity_check(self, scope):
        scope = self.pattern.sanity_check(scope)
        scope = self.expression.sanity_check(scope)
        return scope

class ConstructorChain(ASTNode):
    """A chain of list constructor calls. I.e. x : xs : []."""

    def __init__(self, head, tail):
        self.head = head
        self.tail = tail
    
    def sanity_check(self, scope):
        scope = self.head.sanity_check(scope)
        scope = self.tail.sanity_check(scope)
        return scope

class Pattern(ASTNode):
    """A pattern."""

    def __init__(self, pat):
        self.pat  =  pat

    def sanity_check(self, scope):
        scope = self.pat.sanity_check(scope)
        return scope

class PatternTuple(ASTNode):
    """A tuple-pattern -- i.e. (a, b) or (_, _)."""

    def __init__(self, patterns):
        self.patterns = patterns
    
    def sanity_check(self, scope):
        for pat in self.patterns:
            scope = pat.sanity_check(scope)
        return scope

class PatternList(ASTNode):
    """A list pattern -- i.e. [a, b]."""

    def __init__(self, patterns):
        self.patterns  =  patterns
    
    def sanity_check(self, scope):
        for pat in self.patterns:
            scope = pat.sanity_check(scope)
        return scope

class Alternative(ASTNode):
    """In a match statement, an alternative is one possible pattern match."""

    def __init__(self, pattern, expression):
        self.pattern     =  pattern
        self.expression  =  expression
    
    def sanity_check(self, scope):
        scope = self.sanity_check(self.pattern)
        scope = self.sanity_check(self.expression)
        return scope

class Lambda(ASTNode):
    """A lambda declaration -- e.g. lambda n -> n + 1."""

    def __init__(self, parameters, expression):
        self.parameters  =  parameters
        self.expression  =  expression
    
    def sanity_check(self, scope):
        func_scope = scope + self.parameters
        func_scope = self.expression.sanity_check(func_scope)
        return scope

class Let(ASTNode):
    """A let statement -- we can set identifiers to declarations only for a
    local scope.
    """

    def __init__(self, declarations, expression):
        self.declarations  =  declarations
        self.expression    =  expression
    
    def sanity_check(self, scope):
        let_scope = scope[:]
        for decl in self.declarations:
            let_scope = decl.sanity_check(let_scope)

        let_scope = self.expression.sanity_check(let_scope)
        return scope

class If(ASTNode):
    """An if statement. If 'expression' evaluates to 'true', the 'then'
    expression is used. Otherwise, the 'otherwise' expression is used.
    """

    def __init__(self, expression, then, otherwise):
        self.expression  =  expression
        self.then        =  then
        self.otherwise   =  otherwise
    
    def sanity_check(self, scope):
        scope = self.expression.sanity_check(scope)
        scope = self.then.sanity_check(scope)
        scope = self.otherwise.sanity_check(scope)
        return scope

class Match(ASTNode):
    """A match statement -- like a switch statement that can be used for
    pattern matching.
    """

    def __init__(self, expression, alternatives):
        self.expression    =  expression
        self.alternatives  =  alternatives
    
    def sanity_check(self, scope):
        scope = self.expression.sanity_check(scope)
        for alternative in self.alternatives:
            scope = alternative.sanity_check(scope)
        return scope

class FunctionApplication(ASTNode):
    """Application of a function to an expression. Note that the expression may
    be another function application, resulting in a function that returns a
    function (and allows for 'currying').
    """

    def __init__(self, func, expression):
        self.func        =  func
        self.expression  =  expression
    
    def sanity_check(self, scope):
        scope = self.func.sanity_check(scope)
        scope = self.expression.sanity_check(scope)
        return scope

class Tuple(ASTNode):
    """A tuple of expressions. E.g. (1, 2, 3)."""

    def __init__(self, items):
        self.items  =  items
        self.arity  =  len(items)

    def sanity_check(self, scope):
        for item in self.items:
            scope = item.sanity_check(scope)
        return scope

class List(ASTNode):
    """A list of expressions. E.g. [1, 2, 3]."""

    def __init__(self, items):
        self.items  =  items
    
    def sanity_check(self, scope):
        for item in self.items:
            scope = item.sanity_check(scope)
        return scope

class Parameter(ASTNode):
    """A parameter passed to a function."""

    def __init__(self, name):
        self.name  =  name
    
    def sanity_check(self, scope):
        scope = scope + [self.name]
        return scope

class UsedVar(ASTNode):
    """An object used in some context -- it should exist by the time that it is
    used, otherwise we raise a sanity error.
    """

    def __init__(self, name):
        self.name  =  name
    
    def sanity_check(self, scope):
        if self.name not in scope:
            raise FunkySanityError("Referenced item '{}' expected to " \
                                   "exist.".format(self.name))
        return scope

class Literal(ASTNode):
    """Any literal value. Has a value and a type."""

    def __init__(self, value):
        self.value  =  value
        self.typ    =  python_to_funky[type(value)]
    
    def sanity_check(self, scope):
        return scope # literals are always 'sane' -- return the given scope

class InfixExpression(ASTNode):
    """An infix expression, e.g. 10 * 10. During parsing, we keep these FLAT --
    we perform fixity resolution later, whereby infix expressions become
    instances of FunctionApplications.
    """

    def __init__(self, tokens):
        self.tokens = tokens

    # we do not implement sanity checking here -- it should be performed AFTER
    # fixity resolution.

class BinOpApplication(ASTNode):
    """A binary operator applied to two operands."""

    def __init__(self, operand1, operator, operand2):
        self.operand1 = operand1
        self.operator = operator
        self.operand2 = operand2
    
    def sanity_check(self, scope):
        if type(self.operand1) == str:
            if self.operand1 not in scope:
                raise FunkySanityError("Variable '{}' not defined.".format(self.operand1))
        else:
            scope = self.operand1.sanity_check(scope)

        if type(self.operand2) == str:
            if self.operand2 not in scope:
                raise FunkySanityError("Variable '{}' not defined.".format(self.operand1))
        else:
            scope = self.operand2.sanity_check(scope)

        return scope

class UnaryOpApplication(ASTNode):
    """A unary operator applied to a single operand."""

    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def sanity_check(self, scope):
        scope = self.operand.sanity_check(scope)
        return scope
