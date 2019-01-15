"""Built-in types available for use in Funky."""

from funky.corelang.types import LiteralType
from enum import Enum, auto

# BUILTIN TYPES

BUILTIN_PRIMITIVES = ["Float", "Integer", "Bool", "Char"]

# Mapping of Python types to Funky types.
python_to_funky = {
    float  :  LiteralType("Float"),
    int    :  LiteralType("Integer"),
    bool   :  LiteralType("Bool"),
    str    :  LiteralType("Char"),
}

# BUILTIN FUNCTIONS
# These functions are recognised by the compiler as 'builtin' -- they do not
# need to be defined anywhere.

class Functions(Enum):
    EQUALITY          =  auto()
    INEQUALITY        =  auto()
    LESS              =  auto()
    LEQ               =  auto()
    GREATER           =  auto()
    GEQ               =  auto()
    POW               =  auto()
    PLUS              =  auto()
    MINUS             =  auto()
    TIMES             =  auto()
    DIVIDE            =  auto()
    LIST_CONSTRUCTOR  =  auto()

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
    ":"   :  Functions.LIST_CONSTRUCTOR,
}
