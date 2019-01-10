"""Module containing classes used to represent the abstract syntax tree we get
from parsing the source code. This abstract syntax tree will have the following
operations performed on it:

* Fixity resolution, whereby infix expressions are 'expanded' to properly
  encode associativity and order of operations.
* Renaming, whereby we replace all variable identifiers with machine-given
  names. This process also involves 'sanity checking' the AST -- i.e. making
  sure that duplicate definitions do not exist.

This tree is then 'desugared', resulting in a 'core tree' suitable for
translation.
"""

from funky.frontend import FunkyRenamingError
from funky.util import output_attributes

class ASTNode:
    """Superclass for all abstract syntax tree nodes. Provides a __repr__
    function which allows the nodes to be printed nicely.
    """

    def __init__(self):
        # These booleans represent the operations that have been performed on
        # the parse tree thus far. They are used to ensure that we don't
        # perform the stages in the incorrect order, which could give undefined
        # results.
        self.parsed             =  False
        self.fixities_resolved  =  False
        self.renamed            =  False
        self.desugared          =  False
    
    __repr__ = output_attributes

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

    def __init__(self, identifier, typ):
        self.identifier  =  identifier
        self.typ         =  typ

class NewConsStatement(ASTNode):
    
    def __init__(self, identifier, constructors):
        self.identifier    =  identifier
        self.constructors  =  constructors

class ConstructorPattern(ASTNode):

    def __init__(self, typ, parameters):
        self.typ         =  typ
        self.parameters  =  parameters
        self.arity       =  len(parameters)

    def get_pattern_signature(self):
        return [self.typ, *[p.get_pattern_signature() for p in self.parameters]]

class TypeDeclaration(ASTNode):
    """Node representing a type declaration of some object. e.g.
        'f :: Integer -> Integer' becomes TypeDeclaration('f', ...)
    """

    def __init__(self, identifier, typ):
        self.identifier  =  identifier
        self.typ         =  typ

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
        self.arity       =  len(parameters)

    def get_parameter_signature(self):
        """Multiple definitions for the LHS can exist for implicit pattern
        matching. To distinguish these and make sure that duplicates are
        caught, we generate a parameter signature for each function LHS.
        """
        sig = [self.arity]
        for param in self.parameters:
            sig.append(param.get_pattern_signature())

        return sig

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

    def __init__(self, guard_condition, expression):
        self.guard_condition  =  guard_condition
        self.expression       =  expression

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

    def get_pattern_signature(self):
        return [self.head.get_pattern_signature(), ":"] + \
                [self.tail.get_pattern_signature()]

class Pattern(ASTNode):
    """A pattern."""

    def __init__(self, pat):
        self.pat  =  pat

    def get_pattern_signature(self):
        return self.pat.get_pattern_signature()

class PatternTuple(ASTNode):
    """A tuple-pattern -- i.e. (a, b) or (_, _)."""

    def __init__(self, patterns):
        self.patterns = patterns

    def get_pattern_signature(self):
        return tuple([p.get_pattern_signature() for p in self.patterns])

class PatternList(ASTNode):
    """A list pattern -- i.e. [a, b]."""

    def __init__(self, patterns):
        self.patterns  =  patterns

    def get_pattern_signature(self):
        return [p.get_pattern_signature() for p in self.patterns]

class Alternative(ASTNode):
    """In a match statement, an alternative is one possible pattern match."""

    def __init__(self, pattern, expression):
        self.pattern     =  pattern
        self.expression  =  expression

class Lambda(ASTNode):
    """A lambda declaration -- e.g. lambda n -> n + 1."""

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

class Parameter(ASTNode):
    """A parameter passed to a function."""

    def __init__(self, name):
        self.name  =  name
    
    def get_pattern_signature(self):
        return "PARAM"

class Literal(ASTNode):

    def __init__(self, value):
        self.value = value
    
    def get_pattern_signature(self):
        return self.value

class UsedVar(ASTNode):
    """An object used in some context -- it should exist by the time that it is
    used, otherwise we raise a renaming error.
    """

    def __init__(self, name):
        self.name  =  name
    
class InfixExpression(ASTNode):
    """An infix expression, e.g. 10 * 10. During parsing, we keep these FLAT --
    we perform fixity resolution later, whereby infix expressions become
    instances of FunctionApplications.
    """

    def __init__(self, tokens):
        self.tokens = tokens