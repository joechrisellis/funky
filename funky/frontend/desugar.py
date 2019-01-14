"""We want to 'desugar' the source tree to a simple, core tree. This acts as
our intermediate language. This translation involves, for instance:
    * Expanding if/then statements into case expressions.
    * Expanding pattern guards into case expressions.
    * ...

This module is responsible for doing just that.
"""

import logging

from collections import OrderedDict

from funky.util import get_registry_function, get_unique_varname

from funky.corelang.builtins import Functions
from funky.corelang.coretree import *
from funky.corelang.types import *
from funky.frontend.sourcetree import *
from funky.frontend.rename import get_parameter_name
from funky.frontend.maranget import get_match_tree

from funky.frontend import FunkyDesugarError

log = logging.getLogger(__name__)

desugar = get_registry_function()

@desugar.register(Module)
def module_desugar(node):
    return desugar(node.body)

@desugar.register(ProgramBody)
def program_body_desugar(node):
    # TODO: imports should already be in the parse tree by now, so no need to
    #       do anything with imports.
    toplevel_let = CoreLet([desugar(t) for t in node.toplevel_declarations], None)
    toplevel_let.binds = condense_function_binds(toplevel_let.binds)
    return toplevel_let

@desugar.register(ImportStatement)
def import_statement_desugar(node):
    raise NotImplementedError

@desugar.register(NewTypeStatement)
def new_type_statement_desugar(node):
    typ = desugar(node.typ)
    return CoreBind(node.identifier, typ)

@desugar.register(NewConsStatement)
def new_cons_statement_desugar(node):
    constructors = [desugar(d) for d in node.constructors]
    the_adt = AlgebraicDataType(None, constructors)
    return CoreBind(node.identifier, the_adt)

@desugar.register(Construction)
def construction_desugar(node):
    parameters = [desugar(param) for param in node.parameters]
    return CoreCons(node.constructor, parameters)

@desugar.register(ConstructorType)
def constructor_definition_desugar(node):
    parameters = [desugar(t) for t in node.parameters]
    return CoreCons(node.identifier, parameters)

@desugar.register(TypeDeclaration)
def type_declaration_desugar(node):
    typ = desugar(node.typ)
    return CoreBind(node.identifier, typ)

@desugar.register(FunctionDefinition)
def function_definition_desugar(node):
    rhs_expr = desugar(node.rhs) # first, get the expression.
    function_binding = desugar(node.lhs, rhs_expr) # then pass it to lhs
    return function_binding

@desugar.register(FunctionLHS)
def function_lhs_desugar(node, rhs_expr):
    lam = rhs_expr
    for p in reversed(node.parameters):
        lam = CoreLambda(desugar(p), lam)
    lam.original_arity = len(node.parameters)
    binding = CoreBind(node.identifier, lam)
    return binding

@desugar.register(FunctionRHS)
def function_rhs_desugar(node):
    decls = [desugar(d) for d in node.declarations]
    decls = condense_function_binds(decls)

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

    return CoreLet(decls, match) if decls else match

@desugar.register(GuardedExpression)
def guarded_expression_desugar(node):
    cond = desugar(node.guard_condition)
    expr = desugar(node.expression)
    return cond, expr

@desugar.register(PatternDefinition)
def pattern_definition_desugar(node):
    # TODO: e.g. (x, y) = 1, 2
    pat = desugar(node.pattern)
    expr = desugar(node.expression)
    return CoreBind(pat, expr)

@desugar.register(Alternative)
def alternative_desugar(node):
    pat = desugar(node.pattern)
    expression = desugar(node.expression)
    return CoreAlt(pat, expr)

@desugar.register(Lambda)
def lambda_desugar(node):
    lam = desugar(node.expression)
    for p in reversed(node.parameters):
        p = desugar(p)
        if isinstance(p, CoreCons):
            # the parameter is a pattern -- desugar it to a match structure.
            on_match = CoreAlt(p, lam)
            no_match = CoreAlt(CoreVariable("_"), None)
            scrutinee = CoreVariable(get_unique_varname())
            match_structure = CoreMatch(scrutinee, [on_match, no_match])
            lam = CoreLambda(scrutinee, match_structure)
        else:
            lam = CoreLambda(p, lam)

    lam.original_arity = len(node.parameters)
    return lam

@desugar.register(Let)
def let_desugar(node):
    decls = [desugar(d) for d in node.declarations]
    decls = condense_function_binds(decls)
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
    scrutinee = desugar(node.expression)
    alternatives = [desugar(a) for a in node.alternatives]
    return CoreMatch(scrutinee, alternatives)

@desugar.register(FunctionApplication)
def function_application_desugar(node):
    func = desugar(node.func)
    expr = desugar(node.expression)
    return CoreApplication(func, expr)

@desugar.register(Parameter)
@desugar.register(UsedVar)
def variable_desugar(node):
    return CoreVariable(node.name)

@desugar.register(Literal)
def literal_desugar(node):
    return CoreLiteral(node.value)

@desugar.register(CoreCons)
@desugar.register(CoreTuple)
@desugar.register(CoreList)
@desugar.register(Functions)
@desugar.register(BasicType)
@desugar.register(TupleType)
@desugar.register(ListType)
@desugar.register(FunctionType)
def noop_desugar(node):
    # default functions -- we must acknowledge these when we translate to C. No
    # further work here.
    return node

@desugar.register(InfixExpression)
def infix_expression_desugar(node):
    raise RuntimeError("Infix expression nodes exist in the tree -- fixity " \
                       "resolution has not been performed.")

# ---

def condense_function_binds(binds):
    """The renamer has already ensured that the parse tree does not have any
    duplicate definitions. However, implicit pattern matching, such as

        f 0 = True
        f n = False

    does not constitute a duplicate definition and is not flagged by the
    renamer.  This means that there may exist lambda CoreBinds in the desugared
    statements with the same identifier. These are guaranteed to correspond to
    these implicit pattern matches. This function is responsible for finding
    these binds, and condensing the pattern matching down to core match
    statements.
    """
    seen = set()

    # collate CoreBinds with the same identifier in a dictionary mapping
    # identifiers to bindees
    bind_dict = OrderedDict()
    for bind in binds:
        try:
            bind_dict[bind.identifier].append(bind.bindee)
        except KeyError:
            bind_dict[bind.identifier] = [bind.bindee]

    new_desugared_statements = []
    for identifier, bindees in bind_dict.items():
        # if this is not implicit pattern matching, ignore it
        if not isinstance(bindees[0], CoreLambda):
            bind = CoreBind(identifier, bindees[0])
            new_desugared_statements.append(bind)
            continue

        # otherwise, use the maranget algorithm to convert the pattern match
        # into a match statement.
        pattern_matrix = []
        outcomes = []
        variables = [CoreVariable(get_parameter_name(identifier, i))
                     for i in range(bindees[0].original_arity)]

        for bindee in bindees:
            pattern_matrix.append([])
            for i in range(bindee.original_arity):
                pattern_matrix[-1].append(bindee.param)
                bindee = bindee.expr
            outcomes.append(bindee)

        tree = get_match_tree(pattern_matrix[:], variables[:], outcomes[:])
        new_lambda = tree
        for v in reversed(variables):
            new_lambda = CoreLambda(v, new_lambda)

        new_desugared_statements.append(CoreBind(identifier, new_lambda))

    return new_desugared_statements

def do_desugar(source_tree):
    """Desugars the AST, reducing complex syntactic structures down into a
    simple core language for easier translation later. This constitutes
    'intermediate code generation'.
    """
    assert source_tree.parsed and source_tree.fixities_resolved
    log.info("Desugaring parse tree...")
    desugared = desugar(source_tree)
    log.info("Completed desugaring parse tree.")
    return desugared
