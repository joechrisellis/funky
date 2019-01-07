"""Module containing classes used to represent the abstract syntax tree for the
intermediate language.
"""

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
    
    def __init__(self, bind, expr):
        self.binder  =  bind
        self.expr    =  expr

class CoreLet(CoreNode):

    def __init__(self, bind, expr):
        self.bind  =  bind
        self.expr  =  expr

class CoreMatch(CoreNode):
    
    def __init__(self, scrut, match_binder, alts):
        self.scrut         =  scrut
        self.match_binder  =  match_binder
        self.alts          =  alts

class CoreType(CoreNode):

    def __init__(self, typ):
        self.typ = typ

class CoreAlt(CoreNode):
    
    def __init__(self, altcon, binders, expr):
        self.altcon   =  altcon
        # self.binders  =  binders
        self.expr     =  expr

class CoreAltCon(CoreNode):
    pass

class DataAlt(CoreAltCon):
    
    def __init__(self, data_con):
        self.data_con = data_con

class LiteralAlt(CoreAltCon):

    def __init__(self, literal):
        self.literal = literal

class CoreBind(CoreNode):
    pass

class CoreNonRecBind(CoreBind):
    
    def __init__(self, identifier, expr):
        self.identifier  =  identifier
        self.expr        =  expr

class CoreRecBind(CoreBind):
    
    def __init__(self, binds):
        self.binds = binds
