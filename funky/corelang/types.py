"""Types are very much fundamental to functional programming. This module
contains a consistent representation for them.
"""
from itertools import count
from funky.util import output_attributes

def typename_generator():
    for i in count():
        yield "t" + str(i)

get_typename = typename_generator()

class TypeVariable:
    """A type variable. In type inference, this is used as a placeholder for a
    to-be-discovered type, or for parametric polymorphism.
    """

    __repr__ = output_attributes

    def __init__(self):
        self._type_name   =  None  # lazily defined so None for now
        self.instance     =  None  # if type variable refers to a concrete type
        self.constraints  =  None
        self.parent_class =  None

    def accepts(self, t):
        if self.constraints:
            return self.instance is None or \
                   t.instance is None or \
                   t.type_name in self.constraints or \
                   t.constraints == self.constraints
        return True

    @property
    def type_name(self):
        """We assign names lazily, just so that when the signature of a
        function is printed, we get nice ascending numbers.
        """
        if self._type_name:
            return self._type_name
        self._type_name = next(get_typename)
        return self._type_name

    def __str__(self):
        """If we have a concrete type instance, print that.  . Otherwise, use
        our lazy-defined type name.
        """
        if self.instance:
            return str(self.instance)
        if self.parent_class:
            return self.parent_class
        if self.constraints:
            return "{} [{}]".format(self.type_name, "/".join(self.constraints))
        return self.type_name

class TypeOperator:
    """An n-ary type constructor."""

    __repr__ = output_attributes

    def __init__(self, name, types):
        self.type_name     =  name
        self.types         =  types
        self.parent_class  =  None

    def __str__(self):
        if self.parent_class:
            return self.parent_class
        elif len(self.types) == 0: # 0-ary constructor
            return self.type_name
        elif len(self.types) == 2: # binary constructor
            return "({} {} {})".format(str(self.types[0]), self.type_name,
                                       str(self.types[1]))
        else:
            return "({} {})".format(self.type_name, " ".join(str(x) for x in self.types))

class FunctionType(TypeOperator):
    """A function type. Really, a function type is just a slightly extended
    case of a type operator, hence the inheritance. This is a binary
    constructor.
    """

    def __init__(self, input_type, output_type):
        super().__init__("->", [input_type, output_type])
        self.input_type = input_type
        self.output_type = output_type

    def __str__(self):
        return "({} -> {})".format(str(self.input_type), str(self.output_type))

### GET RID OF RUBBISH BELOW SOON

class TupleType:
    """A tuple-type -- e.g. (Integer, Integer)."""

    def __init__(self, types):
        self.types  =  types
        self.arity  =  len(types)

    def __str__(self):
        return str(self.types)

class ListType:
    """A list-type --  e.g. [Integer]."""
    # TODO: refactor this out to an instance of algebraic data type.

    def __init__(self, typ):
        self.typ  =  typ

class AlgebraicDataType:
    """An algebraic data type defined with the 'newcons' keyword. These are
    used in pattern matching.
    """

    __repr__ = output_attributes

    def __init__(self, type_name, type_parameters, constructors):
        self.type_name        =  type_name
        self.type_parameters  =  type_parameters
        self.constructors     =  constructors

    def __str__(self):
        constructors_str = " | ".join(str(constructor)
                                      for constructor in self.constructors)
        params_str = " ".join(self.type_parameters)
        return "{} {} = {}".format(self.type_name, params_str, constructors_str)

class ConstructorType:
    """A constructor type under an algebraic data type."""

    __repr__ = output_attributes

    def __init__(self, identifier, parameters):
        self.identifier  =  identifier
        self.parameters  =  parameters

    def __str__(self):
        parameters_str = " ".join(str(parameter) for parameter in self.parameters)
        return "{} {}".format(str(self.identifier), parameters_str)
