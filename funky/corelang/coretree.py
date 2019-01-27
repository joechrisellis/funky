"""Module containing classes used to represent the abstract syntax tree for the
intermediate language.
"""

from funky.corelang.builtins import python_to_funky
from funky.util import output_attributes

class CoreNode:
    """Superclass."""

    __repr__ = output_attributes

class CoreTypeDefinition(CoreNode):
    """A type definition -- assigning a name to a type."""

    def __init__(self, identifier, typ):
        self.identifier  =  identifier
        self.typ         =  typ
    
    def __str__(self):
        # TODO
        return "{} := {}".format(self.identifier, str(self.typ))

class CoreBind(CoreNode):
    """A bind -- assigning a name to an expression."""

    def __init__(self, identifier, bindee):
        self.identifier  =  identifier
        self.bindee      =  bindee
    
    def __str__(self):
        bindee_str = str(self.bindee)
        return "{} = {}".format(self.identifier, bindee_str)

class CoreCons(CoreNode):
    """A construction -- a constructor applied to a list of parameters."""

    def __init__(self, constructor, parameters, pattern=False):
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

    def __init__(self, identifier):
        self.identifier  =  identifier

    def __str__(self):
        return str(self.identifier)

class CoreLiteral(CoreNode):
    """A literal."""
    
    def __init__(self, value):
        self.value  =  value
        self.typ    =  python_to_funky[type(value)]

    def __str__(self):
        return repr(self.value)

class CoreApplication(CoreNode):
    """Application of an expression (of type function) to an argument."""

    def __init__(self, expr, arg):
        self.expr  =  expr
        self.arg   =  arg

    def __str__(self):
        return "({}) ({})".format(str(self.expr), str(self.arg))

class CoreLambda(CoreNode):
    """An anonymous lambda expression."""
    
    def __init__(self, param, expr):
        self.param  =  param
        self.expr   =  expr
    
    def __str__(self):
        return "lambda {} -> {}".format(str(self.param),
                                        str(self.expr))

class CoreLet(CoreNode):
    """A recursive let binding. A series of (potentially recursive, or mutually
    recursive) bindings to be made available in an expression.
    """

    def __init__(self, binds, expr):
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
        self.scrutinee  =  scrutinee
        self.alts       =  alts
    
    def __str__(self):
        alts_str = "; ".join(str(alt) for alt in self.alts)
        return "match {} of ({})".format(str(self.scrutinee), alts_str)

class CoreAlt(CoreNode):
    """An alternative in a match statement."""
    
    def __init__(self, altcon, expr):
        self.altcon   =  altcon
        self.expr     =  expr
    
    def __str__(self):
        return "{} -> {}".format(str(self.altcon), str(self.expr))

class CoreTuple(CoreNode):
    
    def __init__(self, items):
        self.items  =  tuple(items)
        self.arity  =  len(items)
    
    def __str__(self):
        return str(self.items)

class CoreList(CoreNode):
    
    def __init__(self, items):
        self.items  =  items
    
    def __str__(self):
        return str(self.items)
