"""We want to 'desugar' the source tree to a simple, core tree. This acts as
our intermediate language. This translation involves, for instance:
    * Expanding if/then statements into case expressions.
    * Expanding pattern guards into case expressions.
    * ...

This module is responsible for doing just that.
"""

from collections import OrderedDict

from funky.util import get_registry_function, get_unique_varname
from funky.misc.scope import Scope

from funky.corelang.builtins import Functions
from funky.corelang.coretree import *
from funky.corelang.types import *
from funky.frontend.sourcetree import *

from funky.frontend import FunkyDesugarError

desugar = get_registry_function()

@desugar.register(Module)
def module_desugar(node, scope=Scope()):
    return desugar(node.body, scope)

@desugar.register(ProgramBody)
def program_body_desugar(node, scope):
    # TODO: imports should already be in the parse tree by now, so no need to
    #       do anything with imports.

    # we will end up with a list of binds, type/cons definitions, and type
    # declarations.
    return [desugar(t, scope) for t in node.toplevel_declarations]

@desugar.register(ImportStatement)
def import_statement_desugar(node, scope):
    raise NotImplementedError

@desugar.register(NewTypeStatement)
def new_type_statement_desugar(node, scope):
    typ = desugar(node.typ, scope)
    return CoreBind(node.identifier, typ)

@desugar.register(NewConsStatement)
def new_cons_statement_desugar(node, scope):
    constructors = [desugar(d, scope) for d in node.constructors]
    the_adt = AlgebraicDataType(None, constructors)
    return CoreBind(node.identifier, the_adt)

@desugar.register(ConstructorType)
def constructor_definition_desugar(node, scope):
    parameters = [desugar(t, scope) for t in node.parameters]
    return CoreCons(node.identifier, parameters)

@desugar.register(TypeDeclaration)
def type_declaration_desugar(node, scope):
    typ = desugar(node.typ, scope)
    return CoreTypeDeclaration(node.identifier, typ)

@desugar.register(FunctionDefinition)
def function_definition_desugar(node, scope):
    rhs_expr = desugar(node.rhs, scope) # first, get the expression.
    function_binding = desugar(node.lhs, rhs_expr, scope) # then pass it to lhs
    return function_binding

@desugar.register(FunctionLHS)
def function_lhs_desugar(node, rhs_expr, scope):
    lam = rhs_expr
    for p in reversed(node.parameters):
        lam = CoreLambda(desugar(p, scope), lam)
    return CoreBind(node.identifier, lam)

@desugar.register(FunctionRHS)
def function_rhs_desugar(node, scope):
    decls = [desugar(d, scope) for d in node.declarations]

    if len(node.expressions) == 1:
        expr = desugar(node.expressions[0], scope)
        return CoreLet(decls, expr) if decls else expr

    # convert the guarded expressions into a match statement. To do this,
    # we build up a chain of match statements by traversing the guards in
    # reverse order.
    match = None
    for guarded_expr in reversed(node.expressions):
        scrutinee, expr = desugar(guarded_expr, scope)
        on_true = CoreAlt(CoreLiteral(True), expr)
        on_false = CoreAlt(CoreLiteral(False), match)
        match = CoreMatch(scrutinee, [on_true, on_false])

    return CoreLet(decls, match) if decls else match

@desugar.register(GuardedExpression)
def guarded_expression_desugar(node, scope):
    cond = desugar(node.guard_condition, scope)
    expr = desugar(node.expression, scope)
    return cond, expr

@desugar.register(PatternDefinition)
def pattern_definition_desugar(node, scope):
    # TODO: e.g. (x, y) = 1, 2
    pat = desugar(node.pattern, scope)
    expr = desugar(node.expression, scope)
    return CoreBind(pat, expr)

@desugar.register(ConstructorChain)
def constructor_chain_desugar(node, scope):
    # TODO: create a primitive list type.
    pass

@desugar.register(Alternative)
def alternative_desugar(node, scope):
    pat = desugar(node.pattern, scope)
    expression = desugar(node.expression, scope)
    return CoreAlt(pat, expr)

@desugar.register(Lambda)
def lambda_desugar(node, scope):
    lam = desugar(node.expression, scope)
    for p in reversed(node.parameters):
        p = desugar(p, scope)
        if isinstance(p, CoreCons):
            # the parameter is a pattern -- desugar it to a match structure.
            on_match = CoreAlt(p, lam)
            no_match = CoreAlt(CoreVariable("_"), None)
            scrutinee = CoreVariable(get_unique_varname())
            match_structure = CoreMatch(scrutinee, [on_match, no_match])
            lam = CoreLambda(scrutinee, match_structure)
        else:
            lam = CoreLambda(p, lam)
    return lam

@desugar.register(Let)
def let_desugar(node, scope):
    decls = [desugar(d, scope) for d in node.declarations]
    expr = desugar(node.expression, scope)
    return CoreLet(decls, expr)

@desugar.register(If)
def if_desugar(node, scope):
    # we convert all ifs down to match statements.
    scrutinee = desugar(node.expression, scope)
    then = desugar(node.then, scope)
    otherwise = desugar(node.otherwise, scope)

    on_true = CoreAlt(CoreLiteral(True), then)
    on_false = CoreAlt(CoreLiteral(False), otherwise)
    return CoreMatch(scrutinee, [on_true, on_false])

@desugar.register(Match)
def match_desugar(node, scope):
    # TODO: apparently this is quite involved when it comes to pattern matching
    # -- job for tomorrow!
    scrutinee = desugar(node.expression, scope)
    alternatives = [desugar(a, scope) for a in node.alternatives]
    return CoreMatch(scrutinee, alternatives)

@desugar.register(FunctionApplication)
def function_application_desugar(node, scope):
    func = desugar(node.func, scope)
    expr = desugar(node.expression, scope)
    return CoreApplication(func, expr)

@desugar.register(Parameter)
@desugar.register(UsedVar)
def variable_desugar(node, scope):
    return CoreVariable(node.name)

@desugar.register(Literal)
def literal_desugar(node, scope):
    return CoreLiteral(node.value)

@desugar.register(CoreCons)
@desugar.register(CoreTuple)
@desugar.register(CoreList)
@desugar.register(Functions)
@desugar.register(Type)
@desugar.register(TupleType)
@desugar.register(ListType)
@desugar.register(FunctionType)
def noop_desugar(node, scope):
    # default functions -- we must acknowledge these when we translate to C. No
    # further work here.
    return node

@desugar.register(InfixExpression)
def infix_expression_desugar(node, scope):
    raise RuntimeError("Infix expression nodes exist in the tree -- fixity " \
                       "resolution has not been performed.")

# ---

def condense_function_binds(binds):
    """The renamer has already ensured that the parse tree does not have any
    duplicate definitions. However, implicit pattern matching, such as

        f 0 = True
        f n = False

    does not constitue a duplicate definition and is not flagged by the
    renamer.  This means that there may exist lambda CoreBinds in the desugared
    statements with the same identifier. These are guaranteed to correspond to
    these implicit pattern matches. This function is responsible for finding
    these binds, and condensing the pattern matching down to core match
    statements.
    """
    seen = set()

    bind_dict = OrderedDict()
    for bind in binds:
        try:
            bind_dict[bind.identifier].append(bind.bindee)
        except KeyError:
            bind_dict[bind.identifier] = [bind.bindee]

    new_desugared_statements = []
    for identifier, bindee in bind_dict.items():
        pass

def do_desugar(source_tree):
    """Desugars the AST, reducing complex syntactic structures down into a
    simple core language for easier translation later. This constitutes
    'intermediate code generation'.
    """
    assert source_tree.parsed and source_tree.fixities_resolved
    desugared = desugar(source_tree)
    desugared = condense_function_binds(desugared)

    from funky.frontend.maranget import get_match_tree
    print(get_match_tree([[CoreLiteral(0)],
                          [CoreVariable("n")]],
                          [CoreVariable("a")],
                          [1,2]))
    return desugared
