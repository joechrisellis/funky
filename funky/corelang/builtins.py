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

Num1               =  TypeVariable()
Num1.constraints   =  [Float.type_name,  Integer.type_name]
Num1.parent_class  =  "Num"

Num2               =  TypeVariable()
Num2.constraints   =  [Float.type_name,  Integer.type_name]
Num2.parent_class  =  "Num"

Num3               =  TypeVariable()
Num3.constraints   =  [Float.type_name,  Integer.type_name]
Num3.parent_class  =  "Num"

BUILTIN_FUNCTIONS = {
    "=="      :  FunctionType(TypeVariable(), FunctionType(TypeVariable(), Bool)),
    "!="      :  FunctionType(TypeVariable(), FunctionType(TypeVariable(), Bool)),
    "<"       :  FunctionType(Num1, FunctionType(Num2, Bool)),
    "<="      :  FunctionType(Num1, FunctionType(Num2, Bool)),
    ">"       :  FunctionType(Num1, FunctionType(Num2, Bool)),
    ">="      :  FunctionType(Num1, FunctionType(Num2, Bool)),
    "**"      :  FunctionType(Num1, FunctionType(Num2, Num3)),
    "+"       :  FunctionType(Num1, FunctionType(Num2, Num3)),
    "-"       :  FunctionType(Num1, FunctionType(Num2, Num3)),
    "negate"  :  FunctionType(Num1, Num2),
    "*"       :  FunctionType(Num1, FunctionType(Num2, Num3)),
    "/"       :  FunctionType(Num1, FunctionType(Num2, Num3)),
    "%"       :  FunctionType(Num1, FunctionType(Num2, Num3)),
    "and"     :  FunctionType(Bool, FunctionType(Bool, Bool)),
    "or"      :  FunctionType(Bool, FunctionType(Bool, Bool)),
}

# All of the builtins form the default environment.
DEFAULT_ENVIRONMENT = {**BUILTIN_PRIMITIVES, **BUILTIN_FUNCTIONS}
