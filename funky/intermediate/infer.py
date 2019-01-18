"""Type inference."""

import logging
from funky.intermediate import FunkyTypeError
from funky.util import get_registry_function, get_unique_varname
from funky.corelang.coretree import *
from funky.corelang.builtins import Functions
from funky.corelang.types import *

from funky.intermediate.tarjan import create_dependency_graph, \
                                      find_strongly_connected_components

log = logging.getLogger(__name__)

def is_wildcard(x):
    return isinstance(x, CoreVariable) and x.identifier == "_"

def get_new_type_variable():
    return BasicType(get_unique_varname())

def instantiate_for_all(for_all):
    subst = {name : get_new_type_variable() for name in for_all.quantifiers}
    return apply_subst(for_all.typ, subst)

def generalize(env, typ):
    free_env, free_typ = free_typevars_in(env), free_typevars_in(typ)
    quantifiers = free_typ - free_env
    if len(quantifiers) > 0:
        return ForAll(quantifiers, typ)
    else:
        return typ

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
            apply_subst(t1.output_type, subst1),
            apply_subst(t2.output_type, subst1)
        );
        return compose_substitutions(subst1, subst2)
    else:
        raise FunkyTypeError("Type mismatch; I expected {} but found "
                             "{}.".format(t1, t2))

def compose_substitutions(subst1, subst2):
    result = {}
    for k, t in subst2.items():
        result[k] = apply_subst(t, subst1)
    return {**result, **subst1}

def bind(name, typ):
    if isinstance(typ, BasicType) and typ.type_name == name:
        return {}
    elif contains(typ, name):
        raise FunkyTypeError("Type {} refers to itself.".format(typ))
    else:
        return {name : typ}

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

free_typevars_in = get_registry_function()

@free_typevars_in.register(dict)
def free_typevars_in_env(env):
    s = set()
    for t in env.values():
        s |= free_typevars_in(t)
    return s

@free_typevars_in.register(LiteralType)
def free_typevars_in_literal(typ):
    return set()

@free_typevars_in.register(BasicType)
def free_typevars_in_literal(typ):
    return set([typ.type_name])

@free_typevars_in.register(FunctionType)
def free_typevars_in_literal(typ):
    return free_typevars_in(typ.input_type) | free_typevars_in(typ.output_type)

@free_typevars_in.register(ForAll)
def free_typevars_in_for_all(for_all):
    quantifiers = set(for_all.quantifiers)
    free_in_type = free_typevars_in(for_all.typ)
    return free_in_type - quantifiers

apply_subst = get_registry_function()

@apply_subst.register(dict)
def apply_subst_to_env(env, subst):
    new_env = env.copy()
    for name, typ in new_env.items():
        new_env[name] = apply_subst(typ, subst)
    return new_env

@apply_subst.register(ForAll)
def apply_subst_to_for_all(for_all, subst):
    tmp_subst = subst.copy()
    for name in for_all.quantifiers:
        try:
            del tmp_subst[name]
        except KeyError:
            pass
    return ForAll(for_all.quantifiers, apply_subst(for_all.typ, tmp_subst))

@apply_subst.register(LiteralType)
def apply_subst_to_type_literal(typ, subst):
    return typ

@apply_subst.register(BasicType)
def apply_subst_to_type_basic(typ, subst):
    try:
        return subst[typ.type_name]
    except KeyError:
        return typ

@apply_subst.register(FunctionType)
def apply_subst_to_type_function(typ, subst):
    return FunctionType(apply_subst(typ.input_type, subst),
                        apply_subst(typ.output_type, subst))

infer = get_registry_function()

@infer.register(CoreLiteral)
def infer_literal(node, env):
    # the type of a literal is already known -- just return it.
    return node.typ, {}

@infer.register(CoreVariable)
def infer_variable(node, env):
    try:
        env_type = env[node.identifier]
        if isinstance(env_type, ForAll):
            return instantiate_for_all(env_type), {}
        else:
            return env_type, {}
    except KeyError:
        raise FunkyTypeError("Unbound variable '{}'.".format(node.identifier))

@infer.register(CoreLambda)
def infer_lambda(node, env):
    tmp_environment = env.copy()
    new_type_variable = get_new_type_variable()
    tmp_environment[node.param.identifier] = new_type_variable

    body_type, subst = infer(node.expr, tmp_environment)
    inferred_type = FunctionType(apply_subst(new_type_variable, subst),
                                 body_type)

    return inferred_type, subst

@infer.register(CoreApplication)
def infer_application(node, env):
    function_type, subst1 = infer(node.expr, env)
    arg_type, subst2 = infer(node.arg, apply_subst(env, subst1))

    new_var = get_new_type_variable()
    subst3 = compose_substitutions(subst1, subst2)
    subst4 = unify(FunctionType(arg_type, new_var), function_type)

    function_type_1 = apply_subst(function_type, subst4)

    subst5 = compose_substitutions(subst3, subst4)
    subst6 = unify(apply_subst(function_type_1.input_type, subst5),
                   arg_type)

    result_subst = compose_substitutions(subst5, subst6)
    return (apply_subst(function_type_1.output_type, result_subst),
            result_subst)

@infer.register(CoreLet)
def infer_let(node, env):
    subst_sum = {}
    env2 = {}
    for bind in node.binds:
        bindee_type, subst1 = infer(bind.bindee, env)
        env1 = apply_subst(subst1, env)
        bindee_polytype = generalize(env1, bindee_type)
        env2.update(env1)
        env2[bind.identifier] = bindee_polytype
        subst_sum = compose_substitutions(subst_sum, subst1)

    expr_type, subst2 = infer(node.expr, env2)
    subst3 = compose_substitutions(subst_sum, subst2)

    return expr_type, subst3

@infer.register(CoreMatch)
def infer_match(node, env):
    # the scrutinee and the altcons must all have the same type.
    # each alternative in a match statement must have the same type.
    scrutinee_type, subst1 = infer(node.scrutinee, env)
    expr_type = None
    
    # check that all of the altcons have consistent types
    for alt in node.alts:
        if isinstance(alt.altcon, CoreVariable):
            altcon_type, subst2 = scrutinee_type, {}
            env[alt.altcon.identifier] = scrutinee_type
        else:
            altcon_type, subst2 = infer(alt.altcon, env)
        subst3 = unify(scrutinee_type, altcon_type)
        subst1 = compose_substitutions(subst1, compose_substitutions(subst2, subst3))
        apply_subst(env, subst1)

        scrutinee_type = altcon_type

        this_expr_type, subst4 = infer(alt.expr, env)
        if expr_type:
            subst4 = unify(expr_type, this_expr_type)
        expr_type = this_expr_type
        subst1 = compose_substitutions(subst1, subst4)

    return apply_subst(expr_type, subst1), subst1

@infer.register(Functions)
def infer_builtin_function(node, env):
    return FunctionType(LiteralType("Integer"), FunctionType(LiteralType("Integer"), LiteralType("Integer"))), {}

def do_type_inference(core_tree):
    # TODO: sort this out!
    log.info("Performing type inference...")
    graph = create_dependency_graph(core_tree.binds)
    find_strongly_connected_components(graph)
    # print(infer(core_tree, {}))
    log.info("Completed type inference.")
