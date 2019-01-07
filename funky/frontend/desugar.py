"""We want to 'desugar' the source tree to a simple, core tree. This acts as
our intermediate language. This translation involves, for instance:
    * Expanding if/then statements into case expressions.
    * Expanding pattern guards into case expressions.
    * ...

This module is responsible for doing just that.
"""

from funky.util import get_registry_function
from funky.corelang.coretree import *
from funky.frontend.sourcetree import *

desugar = get_registry_function()

@desugar.register(Module)
def module_desugar(node):
    desugar(node.body)

@desugar.register(ProgramBody)
def program_body_desugar(node):
    # TODO: sort out imports at a later date
    # for decl in node.import_statements:
        # desugar(decl)

    # desugar all toplevel bindings and return as a recursive bind.
    bindings = [desugar(decl) for decl in node.toplevel_declarations]
    return CoreRecBind(bindings)

@desugar.register(ImportStatement)
def import_statement_desugar(node):
    # TODO: import all variables from the module into the scope
    pass

@desugar.register(NewTypeStatement)
def new_type_statement_desugar(node):
    desugar(node.typ)

@desugar.register(TypeDeclaration)
def type_declaration_desugar(node):
    desugar(node.identifier)
    desugar(node.typ)

@desugar.register(Type)
def type_desugar(node):
    pass

@desugar.register(TupleType)
def tuple_type_desugar(node):
    for typ in node.types:
        desugar(typ)

@desugar.register(ListType)
def list_type_desugar(node):
    desugar(node.typ)

@desugar.register(FunctionType)
def function_type_desugar(node):
    desugar(node.input_type)
    desugar(node.output_type)

@desugar.register(FunctionDefinition)
def function_definition_desugar(node):
    expr = desugar(node.rhs)
    binding = desugar(node.lhs, expr)
    return binding

@desugar.register(FunctionLHS)
def function_lhs_desugar(node, expr):
    lam = Lambda(node.parameters, expr)
    # delegate the desugaring of this lambda, giving us a CoreLambda
    lam = desugar(lam)

    # bind the CoreLambda to the identifier and return
    binding = CoreNonRecBind(node.identifier, lam)
    return binding

@desugar.register(FunctionRHS)
def function_rhs_desugar(node):
    # if we have guarded expressions, we need to convert them to a match
    # statement.
    if len(node.expressions) > 1:
        alts = []
        for guarded_expr in node.expressions:
            desugar(guarded_expr)
    else:   
        # no guarded exp
        desugar(node.expressions[0])
        pass

    if node.declarations:
        let = desugar(node.declarations)

@desugar.register(If)
def if_desugar(node):
    scrut = desugar(node.expression)
    then = desugar(node.then)
    otherwise = desugar(node.otherwise)

    match = CoreMatch(
        scrut,
        CoreAlt(LiteralAlt(True), then), # TODO: will need to formalise literals here!
        CoreAlt(LiteralAlt(False), otherwise)
    )

    return match

@desugar.register(Lambda)
def lambda_desugar(node):
    lam = node.expression
    for p in reversed(node.parameters):
        lam = CoreLambda(p, lam)
    return lam

@desugar.register(BinOpApplication)
def bin_op_application_desugar(node):
    # desugar to function application.
    operand1 = desugar(node.operand1)
    operand2 = desugar(node.operand2)
    app = CoreApplication(
        CoreApplication(node.operator, operand1),
        operand2
    )
    return app

def do_desugar(source_tree):
    """Desugars the AST, reducing complex structures down into simpler versions
    for easier translation later.
    """
    assert source_tree.parsed and source_tree.fixities_resolved and \
           source_tree.renamed

    return desugar(source_tree)
