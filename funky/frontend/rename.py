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
from funky.frontend.sourcetree import *
from funky.corelang.types import *
from funky.corelang.coretree import CoreCons, CoreTuple, CoreList

from funky.frontend import FunkyRenamingError

log = logging.getLogger(__name__)

def get_parameter_name(*args):
    return "_".join(str(a) for a in args if a is not None)

class Scope:
    """A scope maps identifiers to arbitrary items."""

    def __init__(self, parent=None, localizer=None):
        self.local = {}
        self.parent = parent
        self.localizer = localizer

    def search(self, item):
        """Searches the local scope for the item.
        Input:
            item -- the item in question
        Returns:
            the corresponding dict item if found, None otherwise
        """
        return self.local.get(item)

    def rsearch(self, item):
        """Recursively searches the scope for an item. First checks if the item
        is in this scope, then recursively searches the parent scope to see if
        it is defined at a higher level.
        Input:
            item -- the item in question
        Output:
            the corresponding dict item if found, None otherwise
        """
        if item in self.local:
            return self.local[item]
        elif self.parent:
            return self.parent.rsearch(item)
        else:
            return None

    def __getitem__(self, key):
        """Recursively searches the scope for a given key and returns it.
        Input:
            key -- the key of the item to search for.
        Returns:
            the corresponding data in the scope.
        """
        return self.rsearch(key)

    def __setitem__(self, key, value):
        """Sets an item in the local scope dict.
        Input:
            key   -- the key of the item
            value -- any auxiliary data you want to add
        """
        self.local[key] = value

    def __contains__(self, item):
        """A scope 'contains' an item (in other words, that item is defined)
        if it can be found with a recursive search.
        Input:
            item -- the item in question
        Returns:
            True if the item is defined in the scope, False otherwise
        """
        return self.rsearch(item) is not None

    def __repr__(self):
        return "({}, parent={})".format(self.local, self.parent) if self.parent \
          else "({})".format(self.local)

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
def construction_rename(node, scope, fname=None, index=None):
    if node.constructor not in scope:
        raise FunkyRenamingError("Constructor '{}' not " \
                                 "defined.".format(node.constructor))
    elif scope[node.constructor] != len(node.parameters):
        print(scope[node.constructor], node)
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

@rename.register(BasicType)
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
    if node.lhs.identifier not in scope.local:
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
def parameter_rename(node, scope, fname=None, index=None, localizer=None):
    if node.name in scope.local and \
       node.name != "_": # _ is the special wildcard variable
        raise FunkyRenamingError("Duplicate definition of parameter " \
                                 "'{}'.".format(node.name))

    newid = get_parameter_name(fname, localizer, index) if fname or index or \
                                                        localizer \
            else get_unique_varname()

    scope[node.name] = newid
    node.name = newid

@rename.register(UsedVar)
def used_var_rename(node, scope):
    if node.name not in scope:
        raise FunkyRenamingError("Referenced item '{}' does not " \
                                 "exist.".format(node.name))

    node.name = scope[node.name]
    if type(node.name) == dict: # edge case for functions
        node.name = node.name["id"]

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
    logging.info("Renaming and sanity checking parse tree...")
    scope = Scope()
    rename(source_tree, scope)
    source_tree.renamed = True
    logging.info("Renaming and sanity checking parse tree completed.")

    print(source_tree)
