"""Module containing classes used to represent the abstract syntax tree
for the intermediate language.
"""

from funky.corelang.builtins import python_to_funky
from funky.util import output_attributes

class CoreNode:
    """Superclass."""

    __repr__ = output_attributes

    def __init__(self):
        self.inferred_type = None # filled in when type inference is performed

class CoreTypeDefinition(CoreNode):
    """A type definition -- assigning a name to a type."""

    def __init__(self, identifier, typ):
        super().__init__()
        self.identifier  =  identifier
        self.typ         =  typ
    
    def __str__(self):
        # TODO
        return "{} := {}".format(self.identifier, str(self.typ))

class CoreBind(CoreNode):
    """A bind -- assigning a name to an expression."""

    def __init__(self, identifier, bindee):
        super().__init__()
        self.identifier  =  identifier
        self.bindee      =  bindee
    
    def __str__(self):
        bindee_str = str(self.bindee)
        return "{} = {}".format(self.identifier, bindee_str)

class CoreCons(CoreNode):
    """A construction -- a constructor applied to a list of parameters."""

    def __init__(self, constructor, parameters, pattern=False):
        super().__init__()
        self.constructor  =  constructor
        self.parameters   =  parameters

        # set to true when this is used in the context of pattern matching
        self.pattern      =  pattern
    
    def __str__(self):
        parameters_str = " ".join(str(param) for param in self.parameters)
        return "({} {})".format(self.constructor,
                                parameters_str)

class CoreVariable(CoreNode):
    """A reference to a defined variable."""

    def __init__(self, identifier, is_parameter):
        super().__init__()
        self.identifier     =  identifier
        self.free           =  None
        self.is_parameter   =  is_parameter

    def __str__(self):
        return ("param:" if self.is_parameter else "") + str(self.identifier)

class CoreLiteral(CoreNode):
    """A literal."""
    
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return repr(self.value)

class CoreApplication(CoreNode):
    """Application of an expression (of type function) to an argument."""

    def __init__(self, expr, arg):
        super().__init__()
        self.expr  =  expr
        self.arg   =  arg

    def __str__(self):
        return "({}) ({})".format(str(self.expr), str(self.arg))

class CoreLambda(CoreNode):
    """An anonymous lambda expression."""
    
    def __init__(self, param, expr):
        super().__init__()
        self.param          =  param
        self.expr           =  expr

        # was this lambda *explicitly* a lambda as declared in the syntax?
        # i.e. was it (lambda x -> x), or was it f x = x but converted to a
        # core lambda? We need to remember this so that we know not to attempt
        # to condense raw lambdas like we do with implicit pattern matching.
        self.is_raw_lambda  =  False
    
    def __str__(self):
        return "lambda {} -> {}".format(str(self.param),
                                        str(self.expr))

class CoreLet(CoreNode):
    """A recursive let binding. A series of (potentially recursive, or mutually
    recursive) bindings to be made available in an expression.
    """

    def __init__(self, binds, expr):
        super().__init__()
        self.binds  =  binds
        self.expr   =  expr

    def __str__(self):
        binds_str = "; ".join(str(bind) for bind in self.binds)
        return "let {} in {}".format(binds_str, str(self.expr))

class CoreMatch(CoreNode):
    """A match statement -- matching a scrutinee against a series
    of alternatives.
    """
    
    def __init__(self, scrutinee, alts):
        super().__init__()
        self.scrutinee  =  scrutinee
        self.alts       =  alts
    
    def __str__(self):
        alts_str = "; ".join(str(alt) for alt in self.alts)
        return "match {} of ({})".format(str(self.scrutinee), alts_str)

class CoreAlt(CoreNode):
    """An alternative in a match statement."""
    
    def __init__(self, altcon, expr):
        super().__init__()
        self.altcon   =  altcon
        self.expr     =  expr
    
    def __str__(self):
        return "{} -> {}".format(str(self.altcon), str(self.expr))
