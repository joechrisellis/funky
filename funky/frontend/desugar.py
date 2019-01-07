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
    decls = [desugar(d) for d in node.declarations]

    if len(node.expressions) == 1:
        expr = desugar(node.expressions[0])
        return CoreLet(decls, expr) if decls else expr

    # convert the guarded expressions into a match statement. To do this,
    # we build up a chain of match statements by traversing the guards in
    # reverse order.
    match = None
    for guarded_expr in reversed(node.expressions):
        scrutinee, expr = desugar(guarded_expr)
        on_true = CoreAlt(CoreLiteral(True), expr)
        on_false = CoreAlt(CoreLiteral(False), match)
        match = CoreMatch(scrutinee, [on_true, on_false])

    return CoreLet(decls, match) if decls else expr

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
    # TODO: create a primitive list type.
    pass

@desugar.register(Pattern)
def pattern_desugar(node):
    return desugar(node.pat)

@desugar.register(PatternTuple)
def pattern_tuple_desugar(node):
    return TupleType(node.items)

@desugar.register(PatternList)
def pattern_list_desugar(node):
    return ListType(node.items)

@desugar.register(Alternative)
def alternative_desugar(node):
    pat = desugar(node.pattern)
    expression = desugar(node.expression)
    alt_con = DataAlt(pat)
    return CoreAlt(alt_con, expr)

@desugar.register(Lambda)
def lambda_desugar(node):
    lam = desugar(node.expression)
    for p in reversed(node.parameters):
        lam = CoreLambda(desugar(p), lam)
    return lam

@desugar.register(Let)
def let_desugar(node):
    decls = [desugar(d) for d in node.declarations]
    expr = desugar(node.expression)
    return CoreLet(decls, expr)

@desugar.register(If)
def if_desugar(node):
    # we convert all ifs down to match statements.
    scrutinee = desugar(node.expression)
    then = desugar(node.then)
    otherwise = desugar(node.otherwise)

    on_true = CoreAlt(CoreLiteral(True), then)
    on_false = CoreAlt(CoreLiteral(False), otherwise)
    return CoreMatch(scrutinee, [on_true, on_false])

@desugar.register(Match)
def match_desugar(node):
    # TODO: apparently this is quite involved when it comes to pattern matching
    # -- job for tomorrow!
    pass

@desugar.register(FunctionApplication)
def function_application_desugar(node):
    func = desugar(node.func)
    expr = desugar(node.expression)
    return CoreApplication(func, expr)

@desugar.register(CoreTuple)
def tuple_desugar(node):
    return node # tuples are already 'core' from the parser

@desugar.register(CoreList)
def list_desugar(node):
    return node # lists are already 'core' from the parser

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
    # default functions -- we must acknowledge these when we translate to C. No
    # further work here.
    return node

@desugar.register(InfixExpression)
def infix_expression_desugar(node):
    raise RuntimeError("Infix expression nodes exist in the tree -- fixity " \
                       "resolution has not been performed.")

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
