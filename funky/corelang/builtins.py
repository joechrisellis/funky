"""Built-in types available for use in Funky."""

from funky.corelang.types import TypeVariable, TypeOperator, FunctionType
from enum import Enum, auto

# BUILTIN TYPES
BUILTIN_PRIMITIVES = {
    "Float"    :  TypeOperator("Float",    []),
    "Integer"  :  TypeOperator("Integer",  []),
    "Bool"     :  TypeOperator("Bool",     []),
    "String"   :  TypeOperator("String",   []),
}

# purely for easy typing
Float    =  BUILTIN_PRIMITIVES["Float"]
Integer  =  BUILTIN_PRIMITIVES["Integer"]
Bool     =  BUILTIN_PRIMITIVES["Bool"]
String   =  BUILTIN_PRIMITIVES["String"]

# Mapping of Python types to Funky types.
python_to_funky = {
    float  :  Float,
    int    :  Integer,
    bool   :  Bool,
    str    :  String,
}

Stringable               =  TypeVariable()
Stringable.constraints   =  [Float.type_name,  Integer.type_name,  Bool.type_name]
Stringable.parent_class  =  "Stringable"

Intable                  =  TypeVariable()
Intable.constraints      =  [Float.type_name,  Bool.type_name,  String.type_name]
Intable.parent_class     =  "Intable"

Floatable                =  TypeVariable()
Floatable.constraints    =  [Integer.type_name,  String.type_name]
Floatable.parent_class   =  "Floatable"

Num                      =  TypeVariable()
Num.constraints          =  [Float.type_name, Integer.type_name]
Num.parent_class         =  "Num"

# hardly important -- kept for easy lookup of typeclasses where needed
# used to give info about typeclasses with :typeclass command in REPL
TYPECLASSES = {
    "Floatable"   :  Floatable,
    "Intable"     :  Intable,
    "Num"         :  Num,
    "Stringable"  :  Stringable,
}

t = TypeVariable()
BUILTIN_FUNCTIONS = {
    "=="          :  FunctionType(t, FunctionType(t, Bool)),
    "!="          :  FunctionType(t, FunctionType(t, Bool)),
    "<"           :  FunctionType(Num, FunctionType(Num, Bool)),
    "<="          :  FunctionType(Num, FunctionType(Num, Bool)),
    ">"           :  FunctionType(Num, FunctionType(Num, Bool)),
    ">="          :  FunctionType(Num, FunctionType(Num, Bool)),
    "**"          :  FunctionType(Num, FunctionType(Integer, Num)),
    "+"           :  FunctionType(Num, FunctionType(Num, Num)),
    "++"          :  FunctionType(String, FunctionType(String, String)),
    "-"           :  FunctionType(Num, FunctionType(Num, Num)),
    "negate"      :  FunctionType(Num, Num),
    "*"           :  FunctionType(Num, FunctionType(Num, Num)),
    "/"           :  FunctionType(Num, FunctionType(Num, Num)),
    "%"           :  FunctionType(Integer, FunctionType(Integer, Integer)),
    "and"         :  FunctionType(Bool, FunctionType(Bool, Bool)),
    "or"          :  FunctionType(Bool, FunctionType(Bool, Bool)),
    "to_str"      :  FunctionType(Stringable, String),
    "to_int"      :  FunctionType(Intable, Integer),
    "to_float"    :  FunctionType(Floatable, Float),
    "slice_from"  :  FunctionType(Integer, FunctionType(String, String)),
    "slice_to"    :  FunctionType(Integer, FunctionType(String, String)),

    # The fail function accepts a string and returns an uninstantiated,
    # unconstrained type variable. This will be successfully unified with
    # ANYTHING -- meaning you can use the error function in place of any type.
    # In practice this means a function which returns an integer, but sometimes
    # errors, will type check.
    # This might seem a little strange, but it's how Haskell does it!
    "fail"        :  FunctionType(String, TypeVariable()),
    "undefined"   :  TypeVariable(),
}

# All of the builtins form the default environment.
DEFAULT_ENVIRONMENT = {**BUILTIN_PRIMITIVES, **BUILTIN_FUNCTIONS}
