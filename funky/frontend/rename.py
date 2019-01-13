"""Renamer for the Funky programming language. Renaming is the process of
traversing the entire AST and renaming all user-named variables to machine
generated names. This is guaranteed to eliminate name shadowing. Ensuring that
all names are unique in the syntax tree is 'safer' -- during program
transformation, we know that names cannot capture and the program can be
transformed without changing its meaning.
"""

import logging

from funky.corelang.builtins import Functions, BUILTIN_PRIMITIVES

from funky.util import get_registry_function, get_unique_varname
from funky.misc.scope import Scope
from funky.frontend.sourcetree import *
from funky.corelang.types import *
from funky.corelang.coretree import CoreCons, CoreTuple, CoreList

from funky.frontend import FunkyRenamingError

log = logging.getLogger(__name__)

def get_parameter_name(fname, index):
    return "{}_{}".format(fname, index)

rename = get_registry_function()

@rename.register(Module)
def module_rename(node, scope=Scope()):
    rename(node.body, scope)

@rename.register(ProgramBody)
def program_body_rename(node, scope):
    for decl in node.import_statements:
        rename(decl, scope)

    for decl in node.toplevel_declarations:
        rename(decl, scope)

@rename.register(ImportStatement)
def import_statement_rename(node, scope):
    # TODO: import all variables from the module into the scope
    pass

@rename.register(NewTypeStatement)
def new_type_statement_rename(node, scope):
    if node.identifier in scope or node.identifier in BUILTIN_PRIMITIVES:
        raise FunkyRenamingError("Duplicate type '{}'.".format(node.identifier))
    rename(node.typ, scope)

    scope[node.identifier] = node.identifier

@rename.register(NewConsStatement)
def new_cons_statement_rename(node, scope):
    if node.identifier in scope:
        raise FunkyRenamingError("Duplicate definition of constructor type " \
                                 "'{}'.".format(node.identifier))
    elif node.identifier in BUILTIN_PRIMITIVES:
        raise FunkyRenamingError("Cannot define type with builtin name " \
                                 "'{}'.".format(node.identifier))

    # we don't rename the type, only the variables
    scope[node.identifier] = node.identifier
    
    for cons in node.constructors:
        rename(cons, scope)
    
@rename.register(Construction)
def construction_rename(node, scope):
    if node.constructor not in scope:
        raise FunkyRenamingError("Constructor '{}' not " \
                                 "defined.".format(node.constructor))
    elif scope[node.constructor] != len(node.parameters):
        raise FunkyRenamingError("Expected {} parameters for constructor " \
                                 "'{}'.".format(scope[node.constructor],
                                                node.constructor))
    
    for i, param in enumerate(node.parameters):
        rename(param, scope, fname=node.constructor, index=i)

@rename.register(ConstructorType)
def constructor_type_rename(node, scope):
    # anything goes for the node's identifier itself -- however, the types
    # beneath it must be valid.
    if node.identifier in scope:
        raise FunkyRenamingError("Duplicate usage of constructor " \
                                 "'{}'.".format(node.identifier))

    scope[node.identifier] = len(node.parameters)
    for i, param in enumerate(node.parameters):
        if isinstance(node, Parameter):
            rename(param, scope, fname=node.identifier, index=i)
        else:
            rename(param, scope)

@rename.register(TypeDeclaration)
def type_declaration_rename(node, scope):
    # We do not add the identifier to the scope -- simply defining the type
    # of a variable is not enough to say that it can be used. We handle this
    # further in type checking. We only sanity check the type definition
    # here.
    rename(node.typ, scope)

@rename.register(Type)
def type_rename(node, scope):
    if node.type_name not in scope and node.type_name not in BUILTIN_PRIMITIVES:
        raise FunkyRenamingError("Undefined type '{}'.".format(node.type_name))

@rename.register(TupleType)
def tuple_type_rename(node, scope):
    for typ in node.types:
        rename(typ, scope)

@rename.register(ListType)
def list_type_rename(node, scope):
    rename(node.typ, scope)

@rename.register(FunctionType)
def function_type_rename(node, scope):
    rename(node.input_type, scope)
    rename(node.output_type, scope)

@rename.register(FunctionDefinition)
def function_definition_rename(node, scope):
    if node.lhs.identifier in scope.local:
        scope[node.lhs.identifier][1].append(node.lhs.get_parameter_signature())
    else:
        newid = get_unique_varname()
        scope[node.lhs.identifier] = [newid, [node.lhs.get_parameter_signature()]]

    tmp_scope = Scope(parent=scope)
    rename(node.lhs, tmp_scope)

    node.lhs.identifier = scope[node.lhs.identifier][0]

    tmp_scope2 = Scope(parent=tmp_scope)
    rename(node.rhs, tmp_scope2)

@rename.register(FunctionLHS)
def function_lhs_rename(node, scope):
    sigs = scope[node.identifier][1]
    for sig in sigs:
        if sig[0] != node.arity:
            raise FunkyRenamingError("Definition of '{}' has different " \
                                     "number of parameters than previous " \
                                     "definition.".format(node.identifier))

    for i, param in enumerate(node.parameters):
        if isinstance(param, Parameter):
            rename(param, scope, fname=scope[node.identifier][0], index=i)
        else:
            rename(param, scope)

@rename.register(FunctionRHS)
def function_rhs_rename(node, scope):
    for decl in node.declarations:
        rename(decl, scope)

    for exp in node.expressions:
        rename(exp, scope)

@rename.register(GuardedExpression)
def guarded_expression_rename(node, scope):
    rename(node.guard_condition, scope)
    rename(node.expression, scope)

@rename.register(PatternDefinition)
def pattern_definition_rename(node, scope):
    rename(node.pattern, scope)
    rename(node.expression, scope)

@rename.register(Alternative)
def alternative_rename(node, scope):
    rename(node.pattern, scope)
    rename(node.expression, scope)

@rename.register(Lambda)
def lambda_rename(node, scope):
    tmp_scope = Scope(parent=scope)
    for p in node.parameters:
        rename(p, tmp_scope)
    rename(node.expression, tmp_scope)

@rename.register(Let)
def let_rename(node, scope):
    tmp_scope = Scope(parent=scope)
    for decl in node.declarations:
        rename(decl, tmp_scope)

    rename(node.expression, tmp_scope)

@rename.register(If)
def if_rename(node, scope):
    rename(node.expression, scope)
    rename(node.then, scope)
    rename(node.otherwise, scope)

@rename.register(Match)
def match_rename(node, scope):
    rename(node.expression, scope)
    for alternative in node.alternatives:
        rename(alternative, scope)

@rename.register(FunctionApplication)
def function_application_rename(node, scope):
    rename(node.func, scope)
    rename(node.expression, scope)

@rename.register(CoreTuple)
def tuple_rename(node, scope):
    for item in node.items:
        rename(item, scope)

@rename.register(CoreList)
def list_rename(node, scope):
    for item in node.items:
        rename(item, scope)

@rename.register(Parameter)
def parameter_rename(node, scope, fname=None, index=None):
    if node.name in scope.local and \
       node.name != "_": # _ is the special wildcard variable
        raise FunkyRenamingError("Duplicate definition of parameter " \
                                 "'{}'.".format(node.name))

    newid = get_parameter_name(fname, index) if None not in [fname, index] \
            else get_unique_varname()

    scope[node.name] = newid
    node.name = newid

@rename.register(UsedVar)
def used_var_rename(node, scope):
    if node.name not in scope:
        raise FunkyRenamingError("Referenced item '{}' does not " \
                                 "exist.".format(node.name))

    node.name = scope[node.name]
    if type(node.name) == list: # edge case for functions
        node.name = node.name[0]

# literals and functions are always sane. Nothing to do here.
@rename.register(Literal)
@rename.register(Functions)
def noop_rename(node, scope):
    pass

@rename.register(InfixExpression)
def infix_expression_rename(node, scope):
    # special case -- infix expressions should not even be present when we
    # perform sanity checks, as they should have been factored out by fixity
    # resolution performed earlier. Throw an exception if we enocunter one.
    raise RuntimeError("Fixity resolution should be performed before renaming!")

def do_rename(source_tree):
    """Renames items in the source tree so that they all have a unique name
    Also performs sanity checks such as making sure that duplicate declarations
    don't exist, etc.
    """
    assert source_tree.parsed and source_tree.fixities_resolved
    print(source_tree)
    logging.info("Renaming and sanity checking parse tree...")
    scope = Scope()
    rename(source_tree, scope)
    source_tree.renamed = True
    logging.info("Renaming and sanity checking parse tree completed.")

