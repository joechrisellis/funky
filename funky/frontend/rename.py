"""Renamer for the Funky programming language. Renaming is the process of
traversing the entire AST and renaming all user-named variables to machine
generated names. This is guaranteed to eliminate name shadowing. Ensuring that
all names are unique in the syntax tree is 'safer' -- during program
transformation, we know that names cannot capture and the program can be
transformed without changing its meaning.
"""

import logging

from funky.corelang.builtins import Functions, BUILTIN_PRIMITIVES

from funky.util import get_registry_function
from funky.frontend.sourcetree import *
from funky.corelang.types import *
from funky.corelang.coretree import CoreTuple, CoreList

from itertools import count, product
from string import ascii_lowercase

log = logging.getLogger(__name__)

def string_generator():
    """Generator that yields as many strings as you need. Returns (a, b, ...,
    aa, ab, ...).
    """
    for i in count():
        for t in product(ascii_lowercase, repeat=i+1):
            yield "".join(t)

class Scope:
    """A scope maps identifiers to arbitrary items."""

    def __init__(self, parent=None):
        self.local = {}
        self.parent = parent
        self.varname_gen = parent.varname_gen if parent else string_generator()

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

    def get_unique_id(self):
        return "{}".format(next(self.varname_gen))

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

    newid = scope.get_unique_id()
    scope[node.identifier] = newid
    node.identifier = newid

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
    tmp_scope = Scope(parent=scope)
    rename(node.lhs, tmp_scope)

    if node.lhs.identifier in scope.local:
        scope[node.lhs.identifier][1].append(node.lhs.get_parameter_signature())
    else:
        newid = scope.get_unique_id()
        scope[node.lhs.identifier] = [newid, [node.lhs.get_parameter_signature()]]

    node.lhs.identifier = scope[node.lhs.identifier][0]

    tmp_scope2 = Scope(parent=tmp_scope)
    rename(node.rhs, tmp_scope2)

@rename.register(FunctionLHS)
def function_lhs_rename(node, scope):
    if node.identifier in scope.parent.local:
        sigs = scope[node.identifier][1]
        for sig in sigs:
            if sig == node.get_parameter_signature():
                raise FunkyRenamingError("Duplicate definition of " \
                                         "'{}'.".format(node.identifier))
            elif sig[0] != node.arity:
                raise FunkyRenamingError("Definition of '{}' has different " \
                                         "number of parameters than previous " \
                                         "definition.".format(node.identifier))

    for param in node.parameters:
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

@rename.register(ConstructorChain)
def constructor_chain_rename(node, scope):
    rename(node.head, scope)
    rename(node.tail, scope)

@rename.register(Pattern)
def pattern_rename(node, scope):
    rename(node.pat, scope)

@rename.register(PatternTuple)
def pattern_tuple_rename(node, scope):
    for pat in node.patterns:
        rename(pat, scope)

@rename.register(PatternList)
def pattern_list_rename(node, scope):
    for pat in node.patterns:
        rename(pat, scope)

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
def parameter_rename(node, scope):
    if node.name in scope.local and \
       node.name != "_": # _ is the special wildcard variable
        raise FunkyRenamingError("Duplicate definition of parameter " \
                                 "'{}'.".format(node.name))
    newid = scope.get_unique_id()
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

@rename.register(Literal)
def literal_rename(node, scope):
     # literals are always 'sane'. Nothing to do here.
     pass

@rename.register(Functions)
def builtin_function_rename(node, scope):
     # builtin functions are always 'sane'. Nothing to do here.
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
