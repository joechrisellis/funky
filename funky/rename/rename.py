"""Renamer for the Funky programming language. Renaming is the process of
traversing the entire AST and renaming all user-named variables to machine
generated names. This is guaranteed to eliminate name shadowing. Ensuring that
all names are unique in the syntax tree is 'safer' -- during program
transformation, we know that names cannot capture and the program can be
transformed without changing its meaning.
"""

from itertools import count
import logging

from funky.corelang.builtins import BUILTIN_PRIMITIVES, BUILTIN_FUNCTIONS
from funky.corelang.sourcetree import *
from funky.corelang.types import *

from funky.ds import Scope
from funky.util import get_registry_function, global_counter

from funky.rename import FunkyRenamingError

log = logging.getLogger(__name__)

get_unique_varname = lambda: "v" + str(global_counter())
MAIN = "_main"

def get_parameter_name(*args):
    """Gets an underscore-separated parameter name."""
    return "_".join(str(a) for a in args if a is not None)

rename = get_registry_function()

@rename.register(Module)
def module_rename(node, scope=Scope()):
    rename(node.body, scope)

@rename.register(ProgramBody)
def program_body_rename(node, scope):
    for decl in node.toplevel_declarations:
        rename(decl, scope)

@rename.register(NewTypeStatement)
def new_cons_statement_rename(node, scope):
    if node.identifier in scope:
        raise FunkyRenamingError("Duplicate definition of constructor type " \
                                 "'{}'.".format(node.identifier))
    elif node.identifier in BUILTIN_PRIMITIVES:
        raise FunkyRenamingError("Cannot define type with builtin name " \
                                 "'{}'.".format(node.identifier))

    # we don't rename the type, only the variables
    scope[node.identifier] = node.identifier
    
    tmp_scope_1 = Scope(parent=scope)
    for i, param in enumerate(node.type_parameters):
        tmp_scope_1[param] = get_parameter_name(node.identifier, i)

    tmp_scope_2 = Scope(parent=tmp_scope_1)
    for cons in node.constructors:
        rename(cons, tmp_scope_2)

    scope.local.update(tmp_scope_2.local)
    
@rename.register(Construction)
def construction_rename(node, scope, fname=None, index=None):
    if node.constructor not in scope:
        raise FunkyRenamingError("Constructor '{}' not " \
                                 "defined.".format(node.constructor))
    elif scope[node.constructor]["arity"] != len(node.parameters):
        raise FunkyRenamingError("Expected {} parameters for constructor " \
                                 "'{}'.".format(scope[node.constructor],
                                                node.constructor))
    
    localizer = get_parameter_name(fname, index)
    for i, param in enumerate(node.parameters):
        if isinstance(param, Parameter):
            rename(param, scope, fname=node.constructor, index=i,
                    localizer=localizer)
        elif isinstance(param, Construction):
            rename(param, scope, fname=node.constructor, index=i)
        else:
            rename(param, scope)

@rename.register(ConstructorType)
def constructor_type_rename(node, scope):
    # anything goes for the node's identifier itself -- however, the types
    # beneath it must be valid.
    if node.identifier in scope:
        raise FunkyRenamingError("Duplicate usage of constructor " \
                                 "'{}'.".format(node.identifier))

    scope[node.identifier] = {
        "id"     :  node.identifier,
        "arity"  :  len(node.parameters),
    }
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

@rename.register(TypeVariable)
def type_rename(node, scope):
    if node.type_name not in scope and node.type_name not in BUILTIN_PRIMITIVES:
        raise FunkyRenamingError("Undefined type '{}'.".format(node.type_name))

@rename.register(FunctionType)
def function_type_rename(node, scope):
    rename(node.input_type, scope)
    rename(node.output_type, scope)

@rename.register(FunctionDefinition)
def function_definition_rename(node, scope):
    if node.lhs.identifier not in scope.local:
        if scope.is_pending_definition(node.lhs.identifier):
            newid = scope.get_pending_name(node.lhs.identifier)
            if node.lhs.identifier in scope.pending_definition:
                del scope.pending_definition[node.lhs.identifier]
        else:
            newid = get_unique_varname()
        scope[node.lhs.identifier] = {
            "id"     :  newid,
            "arity"  :  len(node.lhs.parameters)
        }

    tmp_scope = Scope(parent=scope)
    rename(node.lhs, tmp_scope)

    node.lhs.identifier = scope[node.lhs.identifier]["id"]

    tmp_scope2 = Scope(parent=tmp_scope)
    rename(node.rhs, tmp_scope2)

    scope.pending_definition.update(tmp_scope.pending_definition)
    scope.pending_definition.update(tmp_scope2.pending_definition)

@rename.register(FunctionLHS)
def function_lhs_rename(node, scope):
    if scope[node.identifier]["arity"] != len(node.parameters):
        raise FunkyRenamingError("Definition of '{}' has different " \
                                 "number of parameters than previous " \
                                 "definition.".format(node.identifier))

    for i, param in enumerate(node.parameters):
        if isinstance(param, Parameter) or isinstance(param, Construction):
            rename(param, scope, fname=scope[node.identifier]["id"], index=i)
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

@rename.register(VariableDefinition)
def pattern_definition_rename(node, scope):
    rename(node.variable, scope, is_main=isinstance(node.variable, Parameter) and \
           node.variable.name == "main")

    tmp_scope = Scope(parent=scope)
    rename(node.expression, tmp_scope)
    scope.pending_definition.update(tmp_scope.pending_definition)

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
    scope.pending_definition.update(tmp_scope.pending_definition)

@rename.register(Let)
def let_rename(node, scope):
    tmp_scope = Scope(parent=scope)
    for decl in node.declarations:
        rename(decl, tmp_scope)

    rename(node.expression, tmp_scope)
    scope.pending_definition.update(tmp_scope.pending_definition)

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

@rename.register(Parameter)
def parameter_rename(node, scope, fname=None, index=None, localizer=None,
                     is_main=False):
    if node.name == "_": return
    if node.name in scope.local:
        raise FunkyRenamingError("Duplicate definition of parameter " \
                                 "'{}'.".format(node.name))


    if is_main:
        newid = MAIN
    elif scope.is_pending_definition(node.name):
        newid = scope.get_pending_name(node.name)
        if node.name in scope.pending_definition:
            del scope.pending_definition[node.name]
    else:
        newid = get_parameter_name(fname, localizer, index) if fname or index or \
                                                            localizer \
                else get_unique_varname()

    scope[node.name] = newid
    node.name = newid

@rename.register(UsedVar)
def used_var_rename(node, scope):
    if node.name in BUILTIN_FUNCTIONS:
        return

    if node.name not in scope:
        if scope.is_pending_definition(node.name):
            new_name = scope.get_pending_name(node.name)
        else:
            new_name = get_unique_varname()
            scope.pending_definition[node.name] = new_name
        node.name = new_name
        return

    node.name = scope[node.name]
    if type(node.name) == dict: # edge case for functions
        node.name = node.name["id"]

# literals are always sane. Nothing to do here.
@rename.register(Literal)
@rename.register(str) # <- builtin functions
def noop_rename(node, scope):
    pass

@rename.register(InfixExpression)
def infix_expression_rename(node, scope):
    # special case -- infix expressions should not even be present when we
    # perform sanity checks, as they should have been factored out by fixity
    # resolution performed earlier. Throw an exception if we enocunter one.
    raise RuntimeError("Fixity resolution should be performed before renaming!")

def check_scope_for_errors(scope):
    err_msg = "\n".join("Referenced item '{}' was never defined.".format(ident)
                        for ident in scope.pending_definition)
    if err_msg:
        raise FunkyRenamingError(err_msg)

def do_rename(source_tree):
    """Renames items in the source tree so that they all have a unique name
    Also performs sanity checks such as making sure that duplicate declarations
    don't exist, etc.

    :param source_tree: the source tree from parsing
    """
    logging.info("Renaming and sanity checking parse tree...")
    scope = Scope()
    rename(source_tree, scope)

    check_scope_for_errors(scope)
    
    logging.info("Renaming and sanity checking parse tree completed.")
