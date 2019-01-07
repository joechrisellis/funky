"""Built-in types available for use in Funky."""

from enum import Enum, auto

primitives = ["Float", "Integer", "Bool", "Char"]

class Primitives(Enum):
    """Primitive types -- the most 'basic' types available."""
    FLOAT    =  auto()
    INTEGER  =  auto()
    BOOL     =  auto()
    CHAR     =  auto()

# Mapping of Python types to Funky types.
python_to_funky = {
    float  :  Primitives.FLOAT,
    int    :  Primitives.INTEGER,
    bool   :  Primitives.BOOL,
    str    :  Primitives.CHAR,
}

BUILTIN_FUNCTIONS = [
    "add",
    "sub",
    "mul",
    "div",
    "pow",
]
