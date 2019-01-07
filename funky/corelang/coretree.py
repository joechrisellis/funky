"""Module containing classes used to represent the abstract syntax tree for the
intermediate language.
"""

from funky.corelang.builtins import python_to_funky
from funky.util import output_attributes

class CoreNode:
    """Superclass."""

    __repr__ = output_attributes

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
        self.scrutinee     =  scrutinee
        self.alts          =  alts

class CoreTypeDeclaration(CoreNode):

    def __init__(self, identifier, typ):
        self.identifier  =  identifier
        self.typ         =  typ

class CoreAlt(CoreNode):
    
    def __init__(self, altcon, expr):
        self.altcon   =  altcon
        self.expr     =  expr

class CoreAltCon(CoreAlt):
    pass

class DataAlt(CoreAltCon):
    
    def __init__(self, data_con):
        self.data_con = data_con

class LiteralAlt(CoreAltCon):
    """An alternative which eventually boils down to a single literal. I.e. 1
    or 'c'. This kind of alternative is not 'pattern matching' in the
    traditional sense.
    """

    def __init__(self, literal):
        self.literal = literal

class CoreBind(CoreNode):

    def __init__(self, identifier, expr):
        self.identifier  =  identifier
        self.expr        =  expr

class CoreTuple(CoreNode):
    
    def __init__(self, items):
        self.items  =  items
        self.arity  =  len(items)

class CoreList(CoreNode):
    
    def __init__(self, items):
        self.items  =  items
