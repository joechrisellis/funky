from funky.util import add_method
from funky.frontend.ast import *

class Scope:
    """A scope maps identifiers to arbitrary items."""

    def __init__(self, parent=None):
        self.local = {}
        self.parent = parent

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

attr = "sanity_check"

@add_method(Module, attr)
def module_sanity_check(self, scope=Scope()):
    self.body.sanity_check(scope)

@add_method(ProgramBody, attr)
def program_body_sanity_check(self, scope):
    for decl in self.import_statements:
        decl.sanity_check(scope)

    for decl in self.toplevel_declarations:
        decl.sanity_check(scope)

@add_method(ImportStatement, attr)
def import_statement_sanity_check(self, scope):
    # TODO: import all variables from the module into the scope
    pass

@add_method(NewTypeStatement, attr)
def new_type_statement_sanity_check(self, scope):
    if self.identifier in scope or self.identifier in primitives:
        raise FunkySanityError("Duplicate type '{}'.".format(self.identifier))
    self.typ.sanity_check(scope)

    scope[self.identifier] = True

@add_method(TypeDeclaration, attr)
def type_declaration_sanity_check(self, scope):
    # We do not add the identifier to the scope -- simply defining the type
    # of a variable is not enough to say that it can be used. We handle this
    # further in type checking. We only sanity check the type definition
    # here.
    self.typ.sanity_check(scope)

@add_method(Type, attr)
def type_sanity_check(self, scope):
    if self.type_name not in scope and self.type_name not in primitives:
        raise FunkySanityError("Undefined type '{}'.".format(self.type_name))

@add_method(TupleType, attr)
def tuple_type_sanity_check(self, scope):
    for typ in self.types:
        typ.sanity_check(scope)

@add_method(ListType, attr)
def list_type_sanity_check(self, scope):
    self.typ.sanity_check(scope)

@add_method(FunctionType, attr)
def function_type_sanity_check(self, scope):
    self.input_type.sanity_check(scope)
    self.output_type.sanity_check(scope)

@add_method(FunctionDefinition, attr)
def function_definition_sanity_check(self, scope):
    tmp_scope = Scope(parent=scope)
    self.lhs.sanity_check(tmp_scope)

    if self.lhs.identifier in scope.local:
        scope[self.lhs.identifier].append(self.lhs.get_parameter_signature())
    else:
        scope[self.lhs.identifier] = [self.lhs.get_parameter_signature()]

    tmp_scope2 = Scope(parent=tmp_scope)
    self.rhs.sanity_check(tmp_scope2)

@add_method(FunctionLHS, attr)
def function_lhs_sanity_check(self, scope):
    if self.identifier in scope.parent.local:
        sigs = scope[self.identifier]
        for sig in sigs:
            if sig == self.get_parameter_signature():
                raise FunkySanityError("Duplicate definition of " \
                                       "'{}'.".format(self.identifier))
            elif sig[0] != self.arity:
                raise FunkySanityError("Definition of '{}' has different " \
                                       "number of parameters than previous " \
                                       "definition.".format(self.identifier))

    for param in self.parameters:
        param.sanity_check(scope)

@add_method(FunctionRHS, attr)
def function_rhs_sanity_check(self, scope):
    for decl in self.declarations:
        decl.sanity_check(scope)

    for exp in self.expressions:
        exp.sanity_check(scope)

@add_method(GuardedExpression, attr)
def guarded_expression_sanity_check(self, scope):
    for cond in self.guard_conditions:
        cond.sanity_check(scope)

    self.expression.sanity_check(scope)

@add_method(PatternDefinition, attr)
def pattern_definition_sanity_check(self, scope):
    self.pattern.sanity_check(scope)
    self.expression.sanity_check(scope)

@add_method(ConstructorChain, attr)
def constructor_chain_sanity_check(self, scope):
    self.head.sanity_check(scope)
    self.tail.sanity_check(scope)

@add_method(Pattern, attr)
def pattern_sanity_check(self, scope):
    self.pat.sanity_check(scope)

@add_method(PatternTuple, attr)
def pattern_tuple_sanity_check(self, scope):
    for pat in self.patterns:
        pat.sanity_check(scope)

@add_method(PatternList, attr)
def pattern_list_sanity_check(self, scope):
    for pat in self.patterns:
        pat.sanity_check(scope)

@add_method(Alternative, attr)
def alternative_sanity_check(self, scope):
    self.pattern.sanity_check(scope)
    self.expression.sanity_check(scope)

@add_method(Lambda, attr)
def lambda_sanity_check(self, scope):
    tmp_scope = Scope(parent=scope)
    for p in self.parameters:
        p.sanity_check(tmp_scope)
    self.expression.sanity_check(tmp_scope)

@add_method(Let, attr)
def let_sanity_check(self, scope):
    tmp_scope = Scope(parent=scope)
    for decl in self.declarations:
        decl.sanity_check(tmp_scope)

    self.expression.sanity_check(tmp_scope)

@add_method(If, attr)
def if_sanity_check(self, scope):
    self.expression.sanity_check(scope)
    self.then.sanity_check(scope)
    self.otherwise.sanity_check(scope)

@add_method(Match, attr)
def match_sanity_check(self, scope):
    self.expression.sanity_check(scope)
    for alternative in self.alternatives:
        alternative.sanity_check(scope)

@add_method(FunctionApplication, attr)
def function_applicatio_sanity_check(self, scope):
    self.func.sanity_check(scope)
    self.expression.sanity_check(scope)

@add_method(Tuple, attr)
def tuple_sanity_check(self, scope):
    for item in self.items:
        item.sanity_check(scope)

@add_method(List, attr)
def list_sanity_check(self, scope):
    for item in self.items:
        item.sanity_check(scope)

@add_method(Parameter, attr)
def parameter_sanity_check(self, scope):
    if self.name in scope.local and \
       self.name != "_": # _ is the special wildcard variable
        raise FunkySanityError("Duplicate definition of parameter " \
                               "'{}'.".format(self.name))
    scope[self.name] = True

@add_method(UsedVar, attr)
def used_var_sanity_check(self, scope):
    if self.name not in scope:
        raise FunkySanityError("Referenced item '{}' does not " \
                               "exist.".format(self.name))

@add_method(Literal, attr)
def literal_sanity_check(self, scope):
     # literals are always 'sane'. Nothing to do here.
     pass

@add_method(InfixExpression, attr)
def infix_expression_sanity_check(self, scope):
    # special case -- infix expressions should not even be present when we
    # perform sanity checks, as they should have been factored out by fixity
    # resolution performed earlier. Throw an exception if we enocunter one.
    raise RuntimeError("Fixity resolution should be performed before sanity " \
                       "checks!")

@add_method(BinOpApplication, attr)
def bin_op_application_sanity_check(self, scope):
    if type(self.operand1) == str:
        if self.operand1 not in scope:
            raise FunkySanityError("Variable '{}' not defined.".format(self.operand1))
    else:
        self.operand1.sanity_check(scope)

    if type(self.operand2) == str:
        if self.operand2 not in scope:
            raise FunkySanityError("Variable '{}' not defined.".format(self.operand1))
    else:
        self.operand2.sanity_check(scope)

@add_method(UnaryOpApplication, attr)
def unary_op_application_sanity_check(self, scope):
    self.operand.sanity_check(scope)

def do_sanity_check(ast):
    """Performs a sanity check on the parsed syntax tree."""
    assert ast.parsed and ast.fixities_resolved
    scope = Scope()
    getattr(ast, attr)(scope)
