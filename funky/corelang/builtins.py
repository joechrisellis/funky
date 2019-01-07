"""Built-in types available for use in Funky."""

from enum import Enum, auto

# BUILTIN TYPES
# These types are recognised by the compiler as 'builtin' -- they do not need
# to be defined anywhere.

class Primitives(Enum):
    """Primitive types -- the most 'basic' types available."""
    FLOAT    =  auto()
    INTEGER  =  auto()
    BOOL     =  auto()
    CHAR     =  auto()

BUILTIN_PRIMITIVES = {
    "Float"    :  Primitives.FLOAT,
    "Integer"  :  Primitives.INTEGER,
    "Bool"     :  Primitives.BOOL,
    "Char"     :  Primitives.CHAR,
}

# Mapping of Python types to Funky types.
python_to_funky = {
    float  :  Primitives.FLOAT,
    int    :  Primitives.INTEGER,
    bool   :  Primitives.BOOL,
    str    :  Primitives.CHAR,
}

# BUILTIN FUNCTIONS
# These functions are recognised by the compiler as 'builtin' -- they do not
# need to be defined anywhere.

class Functions(Enum):
    EQUALITY      =  auto()
    INEQUALITY    =  auto()
    LESS          =  auto()
    LEQ           =  auto()
    GREATER       =  auto()
    GEQ           =  auto()
    POW           =  auto()
    PLUS          =  auto()
    MINUS         =  auto()
    TIMES         =  auto()
    DIVIDE        =  auto()
    CONSTRUCTOR   =  auto()

BUILTIN_FUNCTIONS = {
    "=="  :  Functions.EQUALITY,
    "!="  :  Functions.INEQUALITY,
    "<"   :  Functions.LESS,
    "<="  :  Functions.LEQ,
    ">"   :  Functions.GREATER,
    ">="  :  Functions.GEQ,
    "**"  :  Functions.POW,
    "+"   :  Functions.PLUS,
    "-"   :  Functions.MINUS,
    "*"   :  Functions.TIMES,
    "/"   :  Functions.DIVIDE,
    ":"   :  Functions.CONSTRUCTOR,
}
