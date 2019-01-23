"""Built-in types available for use in Funky."""

from funky.corelang.types import TypeVariable, TypeOperator, FunctionType
from enum import Enum, auto

# BUILTIN TYPES
BUILTIN_PRIMITIVES = ["Float", "Integer", "Bool", "Char"]

Float = TypeOperator("Float", [])
Integer = TypeOperator("Integer", [])
Bool = TypeOperator("Bool", [])
Char = TypeOperator("Char", [])

# Mapping of Python types to Funky types.
python_to_funky = {
    float  :  Float,
    int    :  Integer,
    bool   :  Bool,
    str    :  Char,
}

BUILTIN_FUNCTIONS = {
    "=="  :  FunctionType(TypeVariable(), FunctionType(TypeVariable(), Bool)),
    "!="  :  FunctionType(TypeVariable(), FunctionType(TypeVariable(), Bool)),
    "<"   :  FunctionType(TypeVariable(), FunctionType(TypeVariable(), Bool)),
    "<="  :  FunctionType(TypeVariable(), FunctionType(TypeVariable(), Bool)),
    ">"   :  FunctionType(TypeVariable(), FunctionType(TypeVariable(), Bool)),
    ">="  :  FunctionType(TypeVariable(), FunctionType(TypeVariable(), Bool)),
    "**"  :  FunctionType(Integer, FunctionType(Integer, Integer)),
    "+"   :  FunctionType(Integer, FunctionType(Integer, Integer)),
    "-"   :  FunctionType(Integer, FunctionType(Integer, Integer)),
    "*"   :  FunctionType(Integer, FunctionType(Integer, Integer)),
    "/"   :  FunctionType(Integer, FunctionType(Integer, Integer)),
    ":"   :  None,
}
