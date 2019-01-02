"""The job of the renamer is to perform a 'sanity check' on the AST generated
from the parsing stage. For instance, this stage involves checking that
function calls have the right number of arguments, rearranging infix
expressions according to the fixity of the operators, spotting duplicate
declarations, generating warnings for unused identifiers, etc etc.

Note that Funky's renamer does not actually perform any renaming. It is only
named as such to be consistent with the stage names of other compiler projects,
such as GHC.
"""

from funky.renamer import FunkyRenamerError

from funky.parser.ast import Module, ProgramBody, ImportStatement,             \
                             NewTypeStatement, TypeDeclaration, Type,          \
                             TupleType, ListType, FunctionType,                \
                             FunctionDefinition, FunctionLHS, FunctionRHS,     \
                             GuardedExpression, PatternDefinition,             \
                             ConstructorChain, Pattern, PatternTuple,          \
                             PatternList, Alternative, Lambda, Let, Match,     \
                             FunctionApplication, Tuple, Literal,              \
                             InfixExpression

from funky.core.types import primitives

action = {
    Module : handle_module,
    ProgramBody: handle_program_body,
    ImportStatement : handle_import_statement,
}

def handle_module(self, module):
    scope = {}
    scope = self.handle_program_body(module.body, scope)
    return scope

def handle_program_body(self, body, scope):
    for decl in body.toplevel_declarations:
        if type(decl) == 
        scope = self.actions[type(decl)](decl, scope)
    return scope

def handle_import_statement(self, imp_stmt, scope):
    # TODO: import the variables in the other file into the current
    # namespace.
    return scope

def handle_newtype_statement(self, newtype_stmt, scope):
    ident, typ = newtype_stmt.identifier, newtype_stmt.typ
    if ident in scope:
        raise FunkyRenamerError("Duplicate type definition!")
    
    if type(typ) == Type:
        scope = handle_type(typ, scope)
    elif type(typ) == TupleType:
        scope = handle_tupletype(typ, scope)
    elif type(typ) == ListType:
        scope = handle_listtype(typ, scope)
    else:
        scope = handle_functiontype(typ, scope)

    return scope

def handle_type_declaration(self, type_decl, scope):
    ident, typ = type_decl.identifier, type_decl.typ
    if ident in self.types:
        raise FunkyRenamerError("Duplicate type declaration!")

    scope = scope + [ident]
    return scope

def handle_tupletype(self, tuple_type, scope):
    for typ in tuple_type.types:
        scope = handle_type(typ, scope)
    return scope

def handle_listtype(self, list_type, scope):
    scope = handle_type(list_type.typ)
    return scope

def handle_type(typ, scope):
    name = typ.type_name
    if typ not in scope and typ not in primitives:
        raise FunkyRenamerError("Unrecognised type '{}'. Make sure it is " \
                                "defined before use.".format(name))

    return scope
