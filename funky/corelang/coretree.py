"""Module containing classes used to represent the abstract syntax tree for the
intermediate language.
"""

from funky.corelang.builtins import python_to_funky
from funky.util import output_attributes

class CoreNode:
    """Superclass."""

    __repr__ = output_attributes

class CoreBind(CoreNode):

    def __init__(self, identifier, bindee):
        self.identifier  =  identifier
        self.bindee      =  bindee

class CoreTypeDeclaration(CoreNode):

    def __init__(self, identifier, typ):
        self.identifier  =  identifier
        self.typ         =  typ

class CoreCons(CoreNode):

    def __init__(self, constructor, parameters):
        self.constructor  =  constructor
        self.parameters   =  parameters

class CoreVariable(CoreNode):

    def __init__(self, identifier):
        self.identifier  =  identifier

class CoreLiteral(CoreNode):
    
    def __init__(self, value):
        self.value  =  value
        self.typ    =  python_to_funky[type(value)]

class CoreApplication(CoreNode):

    def __init__(self, expr, arg):
        self.expr  =  expr
        self.arg   =  arg

class CoreLambda(CoreNode):
    
    def __init__(self, param, expr):
        self.param  =  param
        self.expr   =  expr

class CoreLet(CoreNode):

    def __init__(self, binds, expr):
        self.binds  =  binds
        self.expr   =  expr

class CoreMatch(CoreNode):
    
    def __init__(self, scrutinee, alts):
        self.scrutinee  =  scrutinee
        self.alts       =  alts

class CoreAlt(CoreNode):
    
    def __init__(self, altcon, expr):
        self.altcon   =  altcon
        self.expr     =  expr

class CoreTuple(CoreNode):
    
    def __init__(self, items):
        self.items  =  tuple(items)
        self.arity  =  len(items)

class CoreList(CoreNode):
    
    def __init__(self, items):
        self.items  =  items
