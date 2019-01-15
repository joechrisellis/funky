"""Type inference."""

import logging
from funky.intermediate import FunkyTypeError
from funky.util import get_registry_function, get_unique_varname
from funky.corelang.coretree import *
from funky.corelang.types import *

log = logging.getLogger(__name__)


def get_new_type_variable():
    return BasicType(get_unique_varname())

apply_susbst = get_registry_function()

@apply_subst.register(LiteralType)
def apply_subst(typ, subst):
    return typ

@apply_subst.register(BasicType)
def apply_subst(typ, subst):
    try:
        return subst[typ.type_name]
    except KeyError:
        return typ

@apply_subst.register(FunctionType)
def apply_subst(typ, subst):
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
    inferred_type = FunctionType(apply_subst(subst, new_type_variable),
                                 body_type)

def do_type_inference(core_tree):
    pass
