"""We want to 'desugar' the source tree to a simple, core tree. This acts as
our intermediate language. This translation involves, for instance:
    * Expanding if/then statements into case expressions.
    * Expanding pattern guards into case expressions.
    * ...

This module is responsible for doing just that.
"""

from funky.corelang.builtins import Functions
from funky.corelang.coretree import *
from funky.corelang.types import *
from funky.frontend.sourcetree import *

from funky.util import get_registry_function

desugar = get_registry_function()

@desugar.register(Module)
def module_desugar(node):
    return desugar(node.body)

@desugar.register(ProgramBody)
def program_body_desugar(node):
    # TODO: imports should already be in the parse tree by now, so no need to
    #       do anything with imports.

    # we will end up with a list of binds.
    return [desugar(t) for t in node.toplevel_declarations]

@desugar.register(ImportStatement)
def import_statement_desugar(node):
    raise NotImplementedError

@desugar.register(NewTypeStatement)
def new_type_statement_desugar(node):
    typ = desugar(node.typ)
    return CoreBind(node.identifier, typ)

@desugar.register(TypeDeclaration)
def type_declaration_desugar(node):
    typ = desugar(node.typ)
    return CoreTypeDeclaration(node.identifier, typ)

@desugar.register(Type)
def type_desugar(node):
    # 'Type' is fine as it is. We don't need to desugar it; it is already a
    # minimal representation of a type. See types.py.
    return node

@desugar.register(FunctionDefinition)
def function_definition_desugar(node):
    rhs_expr = desugar(node.rhs) # first, get the expression.
    lam = desugar(node.lhs, rhs_expr) # then pass it to lhs, making a lambda

    return lam

@desugar.register(FunctionLHS)
def function_lhs_desugar(node, rhs_expr):
    lam = rhs_expr
    for p in node.parameters:
        lam = CoreLambda(desugar(p), lam)
    return lam

@desugar.register(FunctionRHS)
def function_rhs_desugar(node):
    if len(node.declarations) == 1:
        decls = desugar(node.declarations[0])
    else:
        decls = CoreRecBind([desugar(d) for d in node.declarations])

    if len(node.expressions) == 1:
        expr = desugar(node.expressions[0])
        return expr
    else:
        # convert the guarded expressions into a match statement. To do this,
        # we build up a chain of match statements by traversing the guards in
        # reverse order.
        match = None
        for guarded_expr in reversed(node.expressions):
            cond, alt = desugar(guarded_expr)
            alts = [alt] + ([match] if match else [])
            match = Match(cond, alts)

        return match

@desugar.register(GuardedExpression)
def guarded_expression_desugar(node):
    cond = desugar(node.guard_condition)
    expr = desugar(node.expression)
    return cond, LiteralAlt(expr)

@desugar.register(PatternDefinition)
def pattern_definition_desugar(node):
    # TODO
    pass

@desugar.register(ConstructorChain)
def constructor_chain_desugar(node):
    # TODO
    pass

@desugar.register(Pattern)
def pattern_desugar(node):
    # TODO
    return desugar(node.pat)

@desugar.register(PatternTuple)
def pattern_tuple_desugar(node):
    # TODO
    pass

@desugar.register(PatternList)
def pattern_list_desugar(node):
    # TODO
    pass

@desugar.register(Alternative)
def alternative_desugar(node):
    # TODO
    pass

@desugar.register(Lambda)
def lambda_desugar(node):
    lam = desugar(node.expression)
    for p in node.parameters[::-1]:
        lam = CoreLambda(desugar(p), lam)
    return lam

@desugar.register(Let)
def let_desugar(node):
    pass

@desugar.register(If)
def if_desugar(node):
    pass

@desugar.register(Match)
def match_desugar(node):
    pass

@desugar.register(FunctionApplication)
def function_application_desugar(node):
    func = desugar(node.func)
    expr = desugar(node.expression)
    return CoreApplication(func, expr)

@desugar.register(Tuple)
def tuple_desugar(node):
    pass

@desugar.register(List)
def list_desugar(node):
    pass

@desugar.register(Parameter)
def parameter_desugar(node):
    return CoreVariable(node.name)

@desugar.register(UsedVar)
def used_var_desugar(node):
    return CoreVariable(node.name)

@desugar.register(Literal)
def literal_desugar(node):
    return CoreLiteral(node.value)

@desugar.register(Functions)
def builtin_function_desugar(node):
    return node # default functions

@desugar.register(InfixExpression)
def infix_expression_desugar(node):
    pass

def do_desugar(source_tree):
    """Desugars the AST, reducing complex syntactic structures down into a
    simple core language for easier translation later. This constitutes
    'intermediate code generation'.
    """
    assert source_tree.parsed and source_tree.fixities_resolved
    print(source_tree)
    desugared = desugar(source_tree)
    print(desugared)
    return desugar(source_tree)
