""" The closest construct to lexically-scoped anonymous functions in C are
function pointers. However, we cannot compile anonymous functions directly to
function pointers because:
* they must be declared at the top-level.
* therefore, they cannot capture local environments. 

The solution is closure conversion. We want to eliminate all free varaibles For
every anonymous lambda, we create an environment structure and force all
variable accesses to go through this structure. Every procedure should then
accept the environment as an argument.
"""
from funky.util import get_registry_function

class Closure:

    def __init__(self, lam, env):
        self.lam = lam
        self.env = env

closure_convert = get_registry_function()

@closure_convert.register(CoreBind)
def closure_convert_bind(node):
    closure_convert(node.bindee)

@closure_convert.register(CoreCons)
def closure_convert_cons(node):
    pass

@closure_convert.register(CoreVariable)
def closure_convert_variable(node):
    pass

@closure_convert.register(CoreLiteral)
def closure_convert_literal(node):
    pass

@closure_convert.register(CoreApplication)
def closure_convert_application(node):
    pass

@closure_convert.register(CoreLambda)
def closure_convert_lambda(node):
    pass

@closure_convert.register(CoreLet)
def closure_convert_let(node):
    pass

@closure_convert.register(CoreMatch)
def closure_convert_match(node):
    pass

@closure_convert.register(CoreAlt)
def closure_convert_alt(node):
    pass

@closure_convert.register(CoreLiteral)
@closure_convert.register(CoreLiteral)
def closure_convert_noop(node):
    pass
