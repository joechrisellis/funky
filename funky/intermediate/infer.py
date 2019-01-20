"""Type inference."""

import logging
from funky.intermediate import FunkyTypeError
from funky.util import get_registry_function, get_unique_varname
from funky.corelang.coretree import *
from funky.corelang.builtins import Functions
from funky.corelang.types import *

from funky.intermediate.tarjan import create_dependency_graph, \
                                      find_strongly_connected_components, \
                                      reorder_bindings

log = logging.getLogger(__name__)

def get_new_type_variable():
    """Returns a new BasicType with a unique variable name."""
    return BasicType(get_unique_varname())

def instantiate_for_all(for_all):
    """Instantiates a ForAll. This involves generating new type variables for
    each quantified variable and substituting them in the body of the ForAll.
    """
    subst = {name : get_new_type_variable() for name in for_all.quantifiers}
    return apply_subst(for_all.typ, subst)

def generalize(env, typ):
    """Generalizes a type -- specifically, takes the free variables in a
    specific type and creates a ForAll that accounts for them. We first check
    if the type variable is not free in the environment, since then we can’t
    generalize since they may be bound to specific types later.
    """
    free_env, free_typ = free_typevars_in(env), free_typevars_in(typ)
    quantifiers = free_typ - free_env
    return ForAll(quantifiers, typ) if len(quantifiers) > 0 else typ

def unify(t1, t2):
    """Unifies two types, effectively checking if they 'fit'. If they do, we
    return a substitution that equates them. Otherwise, we raise an exception
    -- this is a type error.
    """
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
    """Applies the first substitution to the types of the second one and then
    combines the result with the first substitution.
    """
    result = {k : apply_subst(t, subst1) for k, t in subst2.items()}
    return {**result, **subst1}

def bind(name, typ):
    """Returns a substitution that maps a variable name to a type. Raises an
    error if the variable refers to itself.
    """
    if isinstance(typ, BasicType) and typ.type_name == name:
        return {}
    elif contains(typ, name):
        raise FunkyTypeError("Type {} refers to itself.".format(typ))
    else:
        return {name : typ}

contains = get_registry_function()

@contains.register(LiteralType)
def contains_literal(typ, name):
    """Does this literal contain this name? The answer is always no."""
    return False

@contains.register(BasicType)
def contains_basic(typ, name):
    """Does this type contain this name? Only if the type's name is
    identical.
    """
    return typ.type_name == name

@contains.register(FunctionType)
def contains_function(typ, name):
    """Does this function contain this name? Only if either its input or output
    types do.
    """
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
    return set() # literal -- no type variables

@free_typevars_in.register(BasicType)
def free_typevars_in_literal(typ):
    return set([typ.type_name]) # only itself

@free_typevars_in.register(FunctionType)
def free_typevars_in_literal(typ):
    # union of the free type variables in the input type and the output type
    return free_typevars_in(typ.input_type) | free_typevars_in(typ.output_type)

@free_typevars_in.register(ForAll)
def free_typevars_in_for_all(for_all):
    quantifiers = set(for_all.quantifiers)
    free_in_type = free_typevars_in(for_all.typ)
    # everything that's free in the type, except quantifiers
    return free_in_type - quantifiers

apply_subst = get_registry_function()

@apply_subst.register(dict)
def apply_subst_to_env(env, subst):
    new_env = {name : apply_subst(typ, subst) for name, typ in env.items()}
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
    """The type of a literal is already known -- just return it."""
    return node.typ, {}

@infer.register(CoreVariable)
def infer_variable(node, env):
    """If the variable's type is registered in the environment, return it
    (instantiating it first if it is a for-all). Otherwise, throw an error --
    the variable is unbound.
    """
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
    """Add the parameter as a free variable to a temporary environment, then
    infer the type of the body.
    """
    tmp_environment = env.copy()
    new_type_variable = get_new_type_variable()
    tmp_environment[node.param.identifier] = new_type_variable

    body_type, subst = infer(node.expr, tmp_environment)
    inferred_type = FunctionType(apply_subst(new_type_variable, subst),
                                 body_type)

    return inferred_type, subst

@infer.register(CoreApplication)
def infer_application(node, env):
    """Function application -- the input and the output must unify."""
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
    """Slightly more involved -- since this can be a recursive let, we must
    first find the strongly-connected components in the dependency graph
    (mutually recursive functions) and order by dependencies. Type inference
    is performed separately for each strongly-connected component to determine
    the most general type of each definition in that group.
    """

    # We reorder the bindings and collect them by strongly connected components.
    # For each SCC, we run variable instantiate individually.
    for group in reorder_bindings(node.binds):
        group_env = env.copy()
        for bind in group:
            group_env[bind.identifier] = get_new_type_variable()

        for bind in group:
            bindee_type, subst1 = infer(bind.bindee, group_env)
            group_env = apply_subst(group_env, subst1)
            bindee_polytype = generalize(group_env, bindee_type)
            group_env[bind.identifier] = bindee_polytype

        env.update(group_env)

    expr_type, subst2 = infer(node.expr, env)
    return apply_subst(expr_type, subst2), subst2

@infer.register(CoreMatch)
def infer_match(node, env):
    """Infer the type of a match statement. Here, the scrutinee has to have the
    same type as all of the altcons, and the alt expressions must all be of the
    same type.
    """

    # the scrutinee and the altcons must all have the same type.
    # each alternative in a match statement must have the same type.
    scrutinee_type, subst1 = infer(node.scrutinee, env)

    expr_type = None
    for alt in node.alts:
        if isinstance(alt.altcon, CoreVariable):
            new_type_variable = get_new_type_variable()
            altcon_type, subst2 = new_type_variable, {new_type_variable : scrutinee_type}
        else:
            altcon_type, subst2 = infer(alt.altcon, env)

        subst3 = unify(scrutinee_type, altcon_type)
        subst1 = compose_substitutions(subst1, subst2)
        subst1 = compose_substitutions(subst1, subst3)

        env = apply_subst(env, subst1)

        if alt.expr is None:
            continue

        alt_expr_type, subst4 = infer(alt.expr, env)
        alt_expr_type = apply_subst(alt_expr_type, subst4)
        if expr_type:
            subst5 = unify(expr_type, alt_expr_type)
            subst1 = compose_substitutions(subst1, subst5)
        expr_type = alt_expr_type

        subst1 = compose_substitutions(subst1, subst4)

    return apply_subst(expr_type, subst1), subst1

@infer.register(Functions)
def infer_builtin_function(node, env):
    return FunctionType(LiteralType("Integer"),
    FunctionType(LiteralType("Integer"), LiteralType("Integer"))), {}

def do_type_inference(core_tree):
    # TODO: sort this out!
    log.info("Performing type inference...")
    graph = create_dependency_graph(core_tree.binds)
    env = {}
    t, subst = infer(core_tree, env)

    print(t, subst)
    print("\n".join("{} :: {}".format(name, typ) for name, typ in env.items()))
    log.info("Completed type inference.")
