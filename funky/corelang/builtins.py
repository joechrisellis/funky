"""Built-in types available for use in Funky."""

from funky.corelang.types import TypeVariable, TypeOperator, FunctionType
from enum import Enum, auto

# BUILTIN TYPES
BUILTIN_PRIMITIVES = ["Float", "Integer", "Bool", "Char"]
BUILTIN_PRIMITIVES = {
    "Float"    :  TypeOperator("Float",    []),
    "Integer"  :  TypeOperator("Integer",  []),
    "Bool"     :  TypeOperator("Bool",     []),
    "Char"     :  TypeOperator("Char",     []),
}

# purely for easy typing
Float    =  BUILTIN_PRIMITIVES["Float"]
Integer  =  BUILTIN_PRIMITIVES["Integer"]
Bool     =  BUILTIN_PRIMITIVES["Bool"]
Char     =  BUILTIN_PRIMITIVES["Char"]

# Mapping of Python types to Funky types.
python_to_funky = {
    float  :  Float,
    int    :  Integer,
    bool   :  Bool,
    str    :  Char,
}

t    = TypeVariable()
op   = TypeOperator("Cons", (t,))
Cons = TypeOperator("Cons", (op,))


BUILTIN_FUNCTIONS = {
    "=="      :  FunctionType(TypeVariable(), FunctionType(TypeVariable(), Bool)),
    "!="      :  FunctionType(TypeVariable(), FunctionType(TypeVariable(), Bool)),
    "<"       :  FunctionType(TypeVariable(), FunctionType(TypeVariable(), Bool)),
    "<="      :  FunctionType(TypeVariable(), FunctionType(TypeVariable(), Bool)),
    ">"       :  FunctionType(TypeVariable(), FunctionType(TypeVariable(), Bool)),
    ">="      :  FunctionType(TypeVariable(), FunctionType(TypeVariable(), Bool)),
    "**"      :  FunctionType(Integer, FunctionType(Integer, Integer)),
    "+"       :  FunctionType(Integer, FunctionType(Integer, Integer)),
    "-"       :  FunctionType(Integer, FunctionType(Integer, Integer)),
    "negate"  :  FunctionType(Integer, Integer),
    "*"       :  FunctionType(Integer, FunctionType(Integer, Integer)),
    "/"       :  FunctionType(Integer, FunctionType(Integer, Integer)),
    "&&"      :  FunctionType(Bool, FunctionType(Bool, Bool)),
    "||"      :  FunctionType(Bool, FunctionType(Bool, Bool)),
    ":"       :  FunctionType(t, FunctionType(Cons, Cons)),
}
