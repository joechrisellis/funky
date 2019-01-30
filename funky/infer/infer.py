"""Type inference."""

import logging
from funky.infer import FunkyTypeError
from funky.util import get_registry_function
from funky.corelang.coretree import *
from funky.corelang.builtins import *
from funky.corelang.types import *

from funky.infer.tarjan import create_dependency_graph,            \
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
        node.inferred_type = get_fresh(ctx[node.identifier], non_generic)
    except KeyError:
        raise FunkyTypeError("Undefined symbol '{}'.".format(node.identifier))

@infer.register(CoreLiteral)
def infer_literal(node, ctx, non_generic):
    """Infer the type for a core literal. Simply use the mapping from Python
    types to function types to infer the type of the literal.
    """
    node.inferred_type = python_to_funky[type(node.value)]

@infer.register(CoreApplication)
def infer_application(node, ctx, non_generic):
    """Infer the type of a function application."""
    infer(node.expr, ctx, non_generic)
    infer(node.arg, ctx, non_generic)
    app_type = TypeVariable()
    unify(FunctionType(node.arg.inferred_type, app_type),
                       node.expr.inferred_type)
    node.inferred_type = app_type

@infer.register(CoreLambda)
def infer_lambda(node, ctx, non_generic):
    """Infer the type of a lambda expression."""
    arg_type = TypeVariable()
    new_ctx = ctx.copy()
    new_ctx[node.param.identifier] = arg_type
    new_non_generic = non_generic.copy()
    new_non_generic.add(arg_type)
    infer(node.expr, new_ctx, new_non_generic)

    node.inferred_type = FunctionType(arg_type, node.expr.inferred_type)

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
            infer(bind.bindee, new_ctx, new_non_generic)
            unify(new_type, bind.bindee.inferred_type)

    # given what we know about the let definitions, infer the type of the
    # expression
    infer(node.expr, new_ctx, non_generic)
    node.inferred_type = node.expr.inferred_type

@infer.register(CoreMatch)
def infer_match(node, ctx, non_generic):
    """Infer the type of a match statement. Here, the scrutinee has to have the
    same type as all of the altcons, and the alt expressions must all be of the
    same type.
    """
    new_ctx = ctx.copy()
    infer(node.scrutinee, ctx, non_generic)

    node.inferred_type = TypeVariable()
    for alt in node.alts:
        if not alt.expr:
            # this false-positives sometimes -- i.e. when pattern matching a
            # boolean.
            log.warning("Potential non-exhaustive pattern matching detected "
                        "when matching against '{}'.".format(node.scrutinee))
            continue

        if isinstance(alt.altcon, CoreVariable):
            alt.altcon.inferred_type = TypeVariable()
            new_ctx[alt.altcon.identifier] = alt.altcon.inferred_type
        else:
            infer(alt.altcon, new_ctx, non_generic)

        unify(node.scrutinee.inferred_type, alt.altcon.inferred_type)
        infer(alt.expr, new_ctx, non_generic)
        unify(node.inferred_type, alt.expr.inferred_type)

@infer.register(CoreCons)
def infer_cons(node, ctx, non_generic):
    # Occurs in the context of pattern matching always.
    # core cons has a constructor, and a list of parameters
    try:
        typeop = ctx[operator_prefix(node.constructor)]
        for x, y in zip(node.parameters, typeop.types):
            ctx[x.identifier] = y
        node.inferred_type = get_fresh(typeop, non_generic)
    except KeyError:
        raise FunkyTypeError("Undefined constructor "
                             "'{}'.".format(node.constructor))

def get_fresh(typ, non_generic):
    """Make a copy of a type expression. The type is copied, generic variables
    are duplicated, and non-generic variables are shared.

    :param typ: the type expression
    :returns:   a copy of the type expression
    """
    type_map = {}

    def aux(tp):
        p = prune(tp)
        if isinstance(p, TypeVariable):
            if is_generic(p, non_generic):
                if p not in type_map:
                    type_map[p] = TypeVariable()
                    type_map[p].constraints = p.constraints
                    type_map[p].parent_class = p.parent_class
                return type_map[p]
            else:
                return p
        elif isinstance(p, TypeOperator):
            return TypeOperator(p.type_name, [aux(x) for x in p.types],
                                parent_class=p.parent_class)

    return aux(typ)

def unify(type1, type2):
    """Unifies two type variables, making them equivalent if they 'fit' and
    raising an error otherwise.

    :param type1: the first type
    :param type1: the second type
    """
    a, b = prune(type1), prune(type2)
    log.debug("Attempting to unify {} and {}...".format(a, b))
    if isinstance(a, TypeVariable):
        if a != b:
            if occurs_in_type(a, b):
                raise FunkyTypeError("Recursive unification detected, stopping.")
            if not a.accepts(b):
                raise FunkyTypeError("Constraints on {} do not permit "
                                     "{}.".format(a, b))
            a.instance = b
    elif isinstance(a, TypeOperator) and isinstance(b, TypeVariable):
        unify(b, a)
    elif isinstance(a, TypeOperator) and isinstance(b, TypeOperator):
        if (a.type_name != b.type_name or len(a.types) != len(b.types)) and \
           not (a.parent_class and b.parent_class
                and a.parent_class == b.parent_class):
                raise FunkyTypeError("Type mismatch: found {} but expected "
                                     "{}.".format(str(a), str(b)))

        if a.type_name == b.type_name:
            for x, y in zip(a.types, b.types):
                unify(x, y)
    else:
        raise RuntimeError("Python typing error encountered when unifying. "
                           "Cannot perform unification between types {} and "
                           "{}.".format(a, b))

def prune(t):
    """Returns the defining instance of the given type. Also collapses the list
    of type instances.

    :param t: a type expression (only TypeVariable will do anything!)
    :return:  the defining instance of the type, if there is one
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

    :param v:           the variable you want to check whether it is generic
    :param non_generic: a list of known non-generic variables
    :return:            True if the variable is generic, False otherwise
    :rtype:             bool
    """
    return not occurs_in(v, non_generic)

def occurs_in_type(v, typ):
    """Returns true if the given type variable v occurs in the type expression
    typ, false otherwise. You must pre-call prune() on v before attempting to
    run this function.

    :param v:   a type variable
    :param typ: a typ expression
    :return:    True if the given type variable occurs in the type expression,
                False otherwise
    :rtype:     bool
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

    :param t:     a type variable
    :param types: a list of types
    :return:      True if t occurs in any of the types, False otherwise
    :rtype:       bool
    """
    return any(occurs_in_type(t, t2) for t2 in types)

def create_type_alias(typedef, ctx):
    """Creates a type alias within the given context.

    :param typedef: the type definition from the core tree
    :param ctx:     the context to create the type alias in
    """
    log.debug("Creating type alias {}...".format(typedef))
    try:
        ctx[typedef.identifier] = ctx[typedef.typ.identifier]
    except KeyError:
        raise FunkyTypeError("Type '{}' not defined, so it cannot be used in "
                             "a type alias.".format(typedef.typ))

def operator_prefix(s):
    return "OP_{}".format(s)

# Used to map constructors to their parent class. For instance:
# newcons List =Cons Integer List | Nil
# Will mean {"OP_Cons" : "List", "OP_Nil" : "List"}, where OP_ is the operator
# prefix.
typeclass_mapping = {}

def create_algebraic_data_structure(adt, ctx):
    """Creates an algebraic data structure within the given context.
    Specifically, creates a TypeOperator and function returning that type
    operator for each of the alternatives. I.e.
    newcons List = Cons Integer List | Nil yields:

        OP_Cons as binary TypeOperator
        OP_NIL as a nullary TypeOperator
        Cons :: Integer -> List -> List

    where OP_ is the operator prefix.

    :param adt: the algebraic data type object
    :param ctx: the context to create the algebraic data structure in
    """

    log.debug("Creating algebraic data type for {}...".format(adt))

    for constructor in adt.constructors:
        prefixed = operator_prefix(constructor.identifier)
        try:
            typeclass_mapping[adt.type_name].append(prefixed)
        except KeyError:
            typeclass_mapping[adt.type_name] = [prefixed]

        tyvars = []
        constructor_op = TypeOperator(prefixed, tyvars,
                                      parent_class=adt.type_name)

        f = constructor_op
        for p in reversed(constructor.parameters):
            t = TypeVariable()
            t.constraints = typeclass_mapping.get(p, [])
            t.parent_class = adt.type_name if p in typeclass_mapping else None
            tyvars.insert(0, t)

            if p in ctx:
                unify(t, ctx[p])
            elif p not in typeclass_mapping:
                raise FunkyTypeError("Type {} not defined.".format(p))
            f = FunctionType(get_fresh(t, ctx), f)

        ctx[prefixed] = constructor_op
        ctx[constructor.identifier] = f

def create_type(typedef, ctx):
    """Creates a type for use in the inferencer.

    :param typedef: the type definition
    :param ctx:     the context to place the new definition in
    """
    if isinstance(typedef.typ, AlgebraicDataType): # newcons
        create_algebraic_data_structure(typedef.typ, ctx)
    else: # newtype
        create_type_alias(typedef, ctx)

def do_type_inference(core_tree, typedefs):
    """Perform type inference on the core tree.

    :param core_tree: the program statements to perform inference on
    :param typedefs:  any type definitions
    """

    log.info("Performing type inference...")
    graph = create_dependency_graph(core_tree.binds)

    ctx, non_generic = DEFAULT_ENVIRONMENT, set()
    for typedef in typedefs:
        create_type(typedef, ctx)

    infer(core_tree, ctx, non_generic)
    log.info("Completed type inference.")
    log.info("The program has output type {}.".format(core_tree.inferred_type))
