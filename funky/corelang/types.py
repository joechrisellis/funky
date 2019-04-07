"""Types are very much fundamental to functional programming. This module
contains a consistent representation for them.
"""
from itertools import count

import funky.util.specialchars as chars
from funky.util.color import *
from funky.util import output_attributes

def typename_generator():
    for i in count():
        yield "t" + str(i)

get_typename = typename_generator()

def contains_function(t):
    """Checks if a given TypeVariable/TypeOperator contains a function.
    
    :param t: the TypeVariable or TypeOperator to check
    :return:  True if t contains a function, False otherwise
    :rtype:   bool
    """
    if isinstance(t, TypeVariable):
        if t.instance:
            return contains_function(t.instance)
        return False
    elif isinstance(t, TypeOperator):
        return is_function(t) or any(is_function(x) for x in t.types)
    else:
        raise ValueError("contains_function input is not TypeVariable or "
                         "TypeOperator.")

def is_function(t):
    """Checks if a given TypeVariable/TypeOperator is a function.
    
    :param t: the TypeVariable or TypeOperator to check
    :return:  True if t is a function, False otherwise
    :rtype:   bool
    """
    if isinstance(t, TypeVariable):
        if t.instance:
            return is_function(t.instance)
        return False
    elif isinstance(t, FunctionType):
        return True
    elif isinstance(t, TypeOperator):
        return t.type_name == "->"
    else:
        raise ValueError("is_function input is not TypeVariable or "
                         "TypeOperator.")

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
            if isinstance(t, TypeOperator):
                return t.type_name in self.constraints
            elif t.instance:
                return t.type_name in self.constraints
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

    def constraints_str(self):
        return "[accepts: {}]".format("/".join(self.constraints))

    def __str__(self):
        """If we have a concrete type instance, print that. Otherwise, use our
        lazy-defined type name.
        """
        if self.instance:
            return str(self.instance)
        if self.parent_class:
            return COLOR_TYPECLASS(self.parent_class)
        if self.constraints:
            return self.constraints_str()
        return COLOR_TYPEVARIABLE(self.type_name)

class TypeOperator:
    """An n-ary type constructor."""

    __repr__ = output_attributes

    def __init__(self, name, types):
        self.type_name     =  name
        self.types         =  types
        self.parent_class  =  None

    def is_string_free(self):
        for typ in self.types:
            if isinstance(typ, str):
                return False
            elif isinstance(typ, TypeOperator):
                if not typ.is_string_free():
                    return False
        return True

    def __str__(self):
        if not self.is_string_free():
            return "-- preprocessing required --"

        # If this is a function (by some inconsistency elsewhere -- I've had
        # troubles making sure that FunctionTypes don't generalise to
        # TypeOperators where they shouldn't!) delegate to the FunctionType str
        # method.
        # This is more a failsafe than anything.
        if is_function(self):
            return FunctionType.__str__(self)

        if self.parent_class:
            return COLOR_TYPECLASS(self.parent_class)
        elif len(self.types) == 0: # 0-ary constructor
            return COLOR_TYPENAME(self.type_name)
        elif len(self.types) == 2: # binary constructor
            return "({} {} {})".format(str(self.types[0]),
                                       COLOR_TYPENAME(self.type_name),
                                       str(self.types[1]))
        else:
            return "({} {})".format(COLOR_TYPENAME(self.type_name),
                                    " ".join(str(x) for x in self.types))

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
        if not self.is_string_free():
            return "-- preprocessing required --"
        wrap = "({})".format
        left = str(self.input_type)
        if is_function(self.input_type):
            left = wrap(left)
        right = str(self.output_type)
        return "{} {} {}".format(left, COLOR_OPERATOR(chars.C_RIGHTARROW), right)

class AlgebraicDataType:
    """An algebraic data type defined with the 'newtype' keyword. These are
    used in pattern matching.
    """

    __repr__ = output_attributes

    def __init__(self, type_name, constructors):
        self.type_name        =  type_name
        self.constructors     =  constructors

    def __str__(self):
        constructors_str = " | ".join(str(constructor)
                                      for constructor in self.constructors)
        return "{} = {}".format(COLOR_TYPECLASS(self.type_name), constructors_str)

class ConstructorType:
    """A constructor type under an algebraic data type."""

    __repr__ = output_attributes

    def __init__(self, identifier, parameters):
        self.identifier  =  identifier
        self.parameters  =  parameters

    def __str__(self):
        parameters_str = " ".join(COLOR_TYPENAME(str(parameter)) for parameter in
                                  self.parameters)
        return "{} {}".format(str(self.identifier), parameters_str)
