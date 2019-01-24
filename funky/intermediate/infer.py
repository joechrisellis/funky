"""Type inference."""

import logging
from funky.intermediate import FunkyTypeError
from funky.util import get_registry_function
from funky.corelang.coretree import *
from funky.corelang.builtins import *
from funky.corelang.types import *

from funky.intermediate.tarjan import create_dependency_graph,            \
                                      find_strongly_connected_components, \
                                      reorder_bindings

log = logging.getLogger(__name__)

infer = get_registry_function()

@infer.register(CoreVariable)
def infer_variable(node, ctx, non_generic):
    """Infer the type for a core variable. If there is no such variable in the
    current context, we raise an exception. Otherwise, we produce a copy of the
    type expression with get_fresh().
    """
    try:
        return get_fresh(ctx[node.identifier], non_generic)
    except KeyError:
        raise FunkyTypeError("Undefined symbol '{}'.".format(node.identifier))

@infer.register(CoreLiteral)
def infer_variable(node, ctx, non_generic):
    """Infer the type for a core literal. Literals have their type pre-encoded
    from parsing.
    """
    return node.typ

@infer.register(str)
def infer_function(node, ctx, non_generic):
    """Infer the type of a built-in function. These should be pre-defined in
    the environment -- if they are not, the programmer has made a mistake, and
    a runtime error will be raised. This error is never user-caused and is only
    to alert the programmer to a configuration error.
    """
    try:
        return get_fresh(ctx[node], non_generic)
    except KeyError:
        raise FunkyTypeError("Undefined function '{}'.".format(node))

@infer.register(CoreApplication)
def infer_application(node, ctx, non_generic):
    """Infer the type of a function application."""
    expr_type, arg_type = infer(node.expr, ctx, non_generic), \
                          infer(node.arg, ctx, non_generic)
    app_type = TypeVariable()
    unify(FunctionType(arg_type, app_type), expr_type)
    return app_type

@infer.register(CoreLambda)
def infer_lambda(node, ctx, non_generic):
    """Infer the type of a lambda expression."""
    arg_type = TypeVariable()
    new_ctx = ctx.copy()
    new_ctx[node.param.identifier] = arg_type
    new_non_generic = non_generic.copy()
    new_non_generic.add(arg_type)
    result_type = infer(node.expr, new_ctx, new_non_generic)
    return FunctionType(arg_type, result_type)

@infer.register(CoreLet)
def infer_let(node, ctx, non_generic):
    """Infer the type of a recursive let expression. This is somewhat involved.
    We must first find the strongly-connected components (mutually recursive)
    definitions and group them. Then, we must rearrange the bindings into
    reverse dependency order. Then, for each grouping, we generalise. This
    ensures that all definitions have the most general type.
    """
    new_ctx, new_non_generic = ctx.copy(), non_generic.copy()

    # for each strongly-connected component/mutually recursive group...
    for group in reorder_bindings(node.binds):
        # we assign a type-variable to each unique definition.
        types = []
        for bind in group:
            new_type = TypeVariable()
            new_ctx[bind.identifier] = new_type
            new_non_generic.add(new_type)
            types.append(new_type)
        
        # then, for each bind and its type, infer the type and unify it.
        for bind, new_type in zip(group, types):
            defn_type = infer(bind.bindee, new_ctx, new_non_generic)
            unify(new_type, defn_type)
    
    # given what we know about the let definitions, infer the type of the
    # expression
    return infer(node.expr, new_ctx, non_generic)

@infer.register(CoreMatch)
def infer_match(node, ctx, non_generic):
    """Infer the type of a match statement. Here, the scrutinee has to have the
    same type as all of the altcons, and the alt expressions must all be of the
    same type.
    """
    scrutinee_type = infer(node.scrutinee, ctx, non_generic)
    
    return_type = TypeVariable()
    for alt in node.alts:
        altcon_type = TypeVariable() if isinstance(alt.altcon, CoreVariable) \
                 else infer(alt.altcon, ctx, non_generic)

        unify(scrutinee_type, altcon_type)

        alt_expr_type = infer(alt.expr, ctx, non_generic)
        unify(return_type, alt_expr_type)

    return return_type

@infer.register(CoreCons)
def infer_cons(node, ctx, non_generic):
    try:
        typeop = get_fresh(ctx[node.constructor], non_generic)
        for parameter, op in zip(node.parameters, typeop.types):
            typ = infer(parameter, ctx, non_generic)
            unify(typ, op)
        typeop.class_name = "Tree"
        print("!!", typeop, typeop.class_name, type(typeop))
        return typeop
    except KeyError:
        raise FunkyTypeError("Undefined constructor "
                             "'{}'.".format(node.constructor))

def get_fresh(typ, non_generic):
    """Make a copy of a type expression. The type is copied, generic variables
    are duplicated, and non-generic variables are shared.
    """
    type_map = {}

    def aux(tp):
        p = prune(tp)
        if isinstance(p, TypeVariable):
            if is_generic(p, non_generic):
                if p not in type_map:
                    type_map[p] = TypeVariable(class_name=p.class_name,
                                               constraints=p.constraints)
                return type_map.get(p, TypeVariable())
            else:
                return p
        elif isinstance(p, TypeOperator):
            return TypeOperator(p.type_name, [aux(x) for x in p.types],
                                class_name=p.class_name)

    return aux(typ)

def unify(type1, type2):
    """Unifies two type variables, making them equivalent if they 'fit' and
    raising an error otherwise.
    """
    a, b = prune(type1), prune(type2)
    if isinstance(a, TypeVariable):
        if a != b:
            if occurs_in_type(a, b):
                raise FunkyTypeError("Recursive unification detected, stopping.")
            if not a.accepts(b):
                raise FunkyTypeError("Constraints on {} do not permit {}".format(str(a), str(b)))
            a.instance = b
    elif isinstance(a, TypeOperator) and isinstance(b, TypeVariable):
        unify(b, a)
    elif isinstance(a, TypeOperator) and isinstance(b, TypeOperator):
        if a.type_name != b.type_name or len(a.types) != len(b.types):
            raise FunkyTypeError("Type mismatch: found {} but expected "
                                 "{}.".format(str(a), str(b)))

        for x, y in zip(a.types, b.types):
            unify(x, y)
    else:
        raise RuntimeError("Python typing error encountered when unifying!")

def prune(t):
    """Returns the defining instance of the given type. Also collapses the list
    of type instances.
    """
    if isinstance(t, TypeVariable):
        if t.instance is not None:
            t.instance = prune(t.instance)
            return t.instance
    return t

def is_generic(v, non_generic):
    """Returns true if the given variable appears in the list of non-generic
    variables, false otherwise. In other words, returns true if the variable is
    generic, false otherwise.
    """
    return not occurs_in(v, non_generic)

def occurs_in_type(v, typ):
    """Returns true if the given type variable v occurs in the type expression
    typ, false otherwise. You must pre-call prune() on v before attempting to
    run this function.
    """
    pruned_typ = prune(typ)
    if pruned_typ == v:
        return True
    elif isinstance(pruned_typ, TypeOperator):
        return occurs_in(v, pruned_typ.types)
    return False

def occurs_in(t, types):
    """Delegates to occurs_in_type for a list of types. Returns true if t
    occurs in any of the types. False otherwise.
    """
    return any(occurs_in_type(t, t2) for t2 in types)

def create_type_alias(typedef, ctx):
    try:
        ctx[typedef.identifier] = ctx[typedef.typ]
    except KeyError:
        raise FunkyTypeError("Type '{}' not defined, so it cannot be used in "
                             "a type alias.".format(typedef.typ))
    
def create_algebraic_data_structure(typedef, ctx):
    t = TypeOperator(typedef.identifier, [])
    ctx[typedef.identifier] = TypeVariable()
    for alternative in typedef.typ.constructors:
        p = [ctx[i] for i in alternative.parameters]
        alt_op = TypeOperator(alternative.identifier, p)
        ctx[alternative.identifier] = alt_op
        ctx[typedef.identifier].class_name = typedef.identifier
        ctx[typedef.identifier].constraints.append(alt_op)

def create_type(typedef, ctx):
    if isinstance(typedef.typ, AlgebraicDataType): # newcons
        create_algebraic_data_structure(typedef, ctx)
    else: # newtype
        create_type_alias(typedef, ctx)

def do_type_inference(core_tree, typedefs):
    log.info("Performing type inference...")
    graph = create_dependency_graph(core_tree.binds)

    ctx, non_generic = DEFAULT_ENVIRONMENT, set()
    for typedef in typedefs:
        create_type(typedef, ctx)

    t = infer(core_tree, ctx, non_generic)
    log.info("Completed type inference.")
    log.info("The program has output type {}.".format(t))
