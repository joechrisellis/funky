"""Types are very much fundamental to functional programming. This module
contains a consistent representation for them.
"""
from funky.util import output_attributes

class Type:
    """Superclass."""

    def __init__(self, type_name):
        self.type_name  =  type_name
    
    __repr__ = output_attributes

class BasicType(Type):
    """A basic named type -- e.g. Integer."""

    def __init__(self, type_name):
        self.type_name  =  type_name

class TupleType(Type):
    """A tuple-type -- e.g. (Integer, Integer)."""

    def __init__(self, types):
        self.types  =  types
        self.arity  =  len(types)

class ListType(Type):
    """A list-type --  e.g. [Integer]."""
    # TODO: refactor this out to an instance of algebraic data type.

    def __init__(self, typ):
        self.typ  =  typ

class FunctionType(Type):
    """A function type -- e.g. [Integer] -> (Integer -> Integer) -> [Integer]"""

    def __init__(self, input_type, output_type):
        self.input_type   =  input_type
        self.output_type  =  output_type

class AlgebraicDataType(Type):
    """An algebraic data type defined with the 'newcons' keyword. These are
    used in pattern matching.
    """
    
    def __init__(self, context, constructors):
        self.context       =  context
        self.constructors  =  constructors

class ConstructorType(Type):
    """A constructor type under an algebraic data type."""

    def __init__(self, identifier, parameters):
        self.identifier  =  identifier
        self.parameters  =  parameters
