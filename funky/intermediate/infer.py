"""Type inference."""

import logging
from funky.intermediate import FunkyTypeError
from funky.util import get_registry_function, get_unique_varname
from funky.corelang.coretree import *
from funky.corelang.builtins import Functions
from funky.corelang.types import *

log = logging.getLogger(__name__)

testenv = {
    "+" : FunctionType(BasicType("Integer"), BasicType("Integer"))
}

def get_new_type_variable():
    return BasicType(get_unique_varname())

def unify(t1, t2):
    if isinstance(t1, LiteralType) and isinstance(t2, LiteralType) and \
       t1.type_name == t2.type_name:
        return {}
    elif isinstance(t1, BasicType):
        return bind(t1.type_name, t2)
    elif isinstance(t2, BasicType):
        return bind(t2.type_name, t1)
    elif isinstance(t1, FunctionType) and isinstance(t2, FunctionType):
        subst1 = unify(t1.input_type, t2.input_type)
        subst2 = unify(
            apply_subst_to_type(t1.output_type, subst1),
            apply_subst_to_type(t2.output_type, subst1)
        );
        return compose_substitutions(subst1, subst2)
    else:
        raise FunkyTypeError("Type mismatch; I expected {} but found "
                             "{}.".format(t1, t2))

def compose_substitutions(subst1, subst2):
    result = {}
    for k, t in subst2.items():
        result[k] = apply_subst_to_type(t, subst1)
    return {**result, **subst1}

def bind(name, typ):
    if isinstance(typ, BasicType) and typ.type_name == name:
        return {}
    elif contains(typ, name):
        raise FunkyTypeError("Type {} refers to itself.".format(typ))
    else:
        return {name : typ}

def apply_subst_to_env(subst, env):
    new_env = env.copy()
    for name, typ in new_env.items():
        new_env[name] = apply_subst_to_type(typ, subst)
    return new_env

contains = get_registry_function()

@contains.register(LiteralType)
def contains_literal(typ, name):
    return False

@contains.register(BasicType)
def contains_basic(typ, name):
    return typ.type_name == name

@contains.register(FunctionType)
def contains_function(typ, name):
    return contains(typ.input_type, name) or contains(typ.output_type, name)

apply_subst_to_type = get_registry_function()

@apply_subst_to_type.register(LiteralType)
def apply_subst_to_type_literal(typ, subst):
    return typ

@apply_subst_to_type.register(BasicType)
def apply_subst_to_type_basic(typ, subst):
    try:
        return subst[typ.type_name]
    except KeyError:
        return typ

@apply_subst_to_type.register(FunctionType)
def apply_subst_to_type_function(typ, subst):
    return FunctionType(apply_subst_to_type(typ.input_type, subst),
                        apply_subst_to_type(typ.output_type, subst))

infer = get_registry_function()

@infer.register(CoreLiteral)
def infer_literal(node, env):
    # the type of a literal is already known -- just return it.
    return node.typ, {}

@infer.register(CoreVariable)
def infer_variable(node, env):
    try:
        return env[node.identifier], {}
    except KeyError:
        raise FunkyTypeError("Variable '{}' not in "
                             "scope.".format(node.identifier))

@infer.register(CoreLambda)
def infer_lambda(node, env):
    tmp_environment = env.copy()
    new_type_variable = get_new_type_variable()
    tmp_environment[node.param] = new_type_variable

    body_type, subst = infer(tmp_environment, node.expr)
    inferred_type = FunctionType(apply_subst_to_type(subst, new_type_variable),
                                 body_type)

    return inferred_type, subst

@infer.register(CoreApplication)
def infer_application(node, env):
    print(node.expr)
    function_type, subst1 = infer(node.expr, env)
    arg_type, subst2 = infer(node.arg, apply_subst_to_env(subst1, env))

    new_var = get_new_type_variable()
    subst3 = compose_substitutions(subst1, subst2)
    subst4 = unify(FunctionType(arg_type, new_var), function_type)

    function_type_1 = apply_subst_to_type(function_type, subst4)

    subst5 = compose_substitutions(subst3, subst4)
    subst6 = unify(apply_subst_to_type(function_type_1.input_type, subst5),
                   arg_type)

    result_subst = compose_substitutions(subst5, subst6)
    return (apply_subst_to_type(function_type_1.output_type, result_subst),
            result_subst)

@infer.register(CoreMatch)
def infer_match(node, env):
    pass # TODO

@infer.register(Functions)
def infer_builtin_function(node, env):
    return FunctionType(BasicType("Integer"), FunctionType(BasicType("Integer"), BasicType("Integer"))), {}

def do_type_inference(core_tree):
    # TODO: sort this out!
    log.info("Performing type inference...")
    print(infer(core_tree.binds[0].bindee, testenv))
    log.info("Completed type inference.")
