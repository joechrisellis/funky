"""Module containing classes used to represent the abstract syntax tree
for the intermediate language.
"""

import funky.globals

from funky.corelang.builtins import python_to_funky, BUILTIN_FUNCTIONS
from funky.corelang.types import AlgebraicDataType
from funky.ds import Graph

from funky.util.color import *
from funky.util import get_registry_function, output_attributes

class CoreNode:
    """Superclass."""

    __repr__ = output_attributes

    def __init__(self):
        self.inferred_type = None # filled in when type inference is performed

class CoreTypeDefinition(CoreNode):
    """A type definition -- assigning a name to a type."""

    def __init__(self, identifier, typ):
        super().__init__()
        self.identifier  =  identifier
        self.typ         =  typ
    
    def __str__(self):
        return "{}".format(str(self.typ))

class CoreBind(CoreNode):
    """A bind -- assigning a name to an expression."""

    def __init__(self, identifier, bindee):
        super().__init__()
        self.identifier  =  identifier
        self.bindee      =  bindee
    
    def __str__(self):
        bindee_str = str(self.bindee)
        return "{} {} {}".format(self.identifier, COLOR_EQUALS("="), bindee_str)

class CoreCons(CoreNode):
    """A construction -- a constructor applied to a list of parameters."""

    def __init__(self, constructor, parameters, pattern=False):
        super().__init__()
        self.constructor  =  constructor
        self.parameters   =  parameters

        # set to true when this is used in the context of pattern matching
        self.pattern      =  pattern
    
    def __str__(self):
        parameters_str = " ".join(str(param) for param in self.parameters)
        return "({} {})".format(COLOR_TYPENAME(self.constructor),
                                parameters_str)

class CoreVariable(CoreNode):
    """A reference to a defined variable."""

    def __init__(self, identifier):
        super().__init__()
        self.identifier     =  identifier

    def __str__(self):
        # if this is a builtin, color it accordingly
        if self.identifier in BUILTIN_FUNCTIONS:
            return COLOR_OPERATOR(str(self.identifier))
        return str(self.identifier)

class CoreLiteral(CoreNode):
    """A literal."""
    
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return COLOR_CONSTANT(repr(self.value))

class CoreApplication(CoreNode):
    """Application of an expression (of type function) to an argument."""

    def __init__(self, expr, arg):
        super().__init__()
        self.expr  =  expr
        self.arg   =  arg

    def __str__(self):
        return "({}) ({})".format(str(self.expr), str(self.arg))

class CoreLambda(CoreNode):
    """An anonymous lambda expression."""
    
    def __init__(self, param, expr):
        super().__init__()
        self.param          =  param
        self.expr           =  expr

        # was this lambda *explicitly* a lambda as declared in the syntax?
        # i.e. was it (lambda x -> x), or was it f x = x but converted to a
        # core lambda? We need to remember this so that we know not to attempt
        # to condense raw lambdas like we do with implicit pattern matching.
        self.is_raw_lambda  =  False
    
    def __str__(self):
        return "{} {} {} {}".format(COLOR_KEYWORD("lambda"),
                                    str(self.param),
                                    COLOR_OPERATOR("->"),
                                    str(self.expr))

class CoreLet(CoreNode):
    """A recursive let binding. A series of (potentially recursive, or mutually
    recursive) bindings to be made available in an expression.
    """

    tmp_varname = "_let_expr"

    def __init__(self, binds, expr):
        super().__init__()
        self.binds             =  binds
        self.expr              =  expr
        self.create_dependency_graph()

        if funky.globals.CURRENT_MODE != funky.globals.Mode.REPL:
            # NOTE: we prune the definitions BEFORE we condense our function
            # bindings. This might seem out of order, but there is a valid
            # reason: by first pruning away bindings that are unused, we
            # completely avoid performing Maranget's algorithm on bindings that
            # are never used.
            self.prune_bindings()

    def create_dependency_graph(self):
        """Creates a graph representing how the bindings depend on one another.
        For instance, in:

            a = b 10
            b x = x + 1
            c = a
        
        a depends on b, b depends on nothing, and c depends on a.

        :return:         a graph object representing the dependencies
        :rtype:          Graph
        """

        # add a pseudo bind for the expression -- this is the easiest way to
        # show us what the actual expression depends on in the list of
        # bindings, so we can remove anything that's unneeded
        bindings = [*self.binds]
        if funky.globals.CURRENT_MODE != funky.globals.Mode.REPL:
            let_expr = CoreBind(self.tmp_varname, self.expr)
            bindings.append(let_expr)

        graph = Graph()

        ids = set([bind.identifier for bind in bindings])
        for bind in bindings:
            graph.add_node(bind.identifier)
            add_edges(bind.bindee, graph, bind.identifier, ids)

        self.dependency_graph = graph

    def prune_bindings(self):
        """Prunes the core tree by getting rid of any unused bindings."""
        keep, visited = set(), set()

        def dfs(at):
            visited.add(at)
            neighbours = self.dependency_graph.graph[at]
            for to in neighbours:
                if to not in visited:
                    dfs(to)
            keep.add(at)

        dfs(self.tmp_varname) # <- populate our 'keep' variable

        # get rid of any unused bindings, as well as our temporary binding
        new_bindings = [b for b in self.binds if b.identifier in keep and \
                                              not b.identifier == self.tmp_varname]
        self.binds = new_bindings

        # Create the new dependency graph from the old one. Extracts all of the
        # kept variables and their edges.
        new_dependency_graph = Graph()
        for var in keep:
            if var == self.tmp_varname: continue
            new_dependency_graph.graph[var] = self.dependency_graph.graph[var]
        self.dependency_graph = new_dependency_graph

    def __str__(self):
        binds_str = "; ".join(str(bind) for bind in self.binds)
        return "{} {} {} {}".format(COLOR_KEYWORD("let"), binds_str,
                                    COLOR_KEYWORD("in"), str(self.expr))

class CoreMatch(CoreNode):
    """A match statement -- matching a scrutinee against a series
    of alternatives.
    """
    
    def __init__(self, scrutinee, alts):
        super().__init__()
        self.scrutinee  =  scrutinee
        self.alts       =  alts
    
    def __str__(self):
        alts_str = "; ".join(str(alt) for alt in self.alts)
        return "{} {} {} ({})".format(COLOR_KEYWORD("match"),
                                      str(self.scrutinee),
                                      COLOR_KEYWORD("with"),
                                      alts_str)

class CoreAlt(CoreNode):
    """An alternative in a match statement."""
    
    def __init__(self, altcon, expr):
        super().__init__()
        self.altcon   =  altcon
        self.expr     =  expr
    
    def __str__(self):
        return "{} {} {}".format(str(self.altcon), COLOR_OPERATOR("->"),
                                 str(self.expr))

add_edges = get_registry_function()

@add_edges.register(CoreVariable)
def add_edges_variable(bindee, graph, current, ids):
    # We are only concerned about dependencies in our isolated set of bindings
    # -- ignore anything that we're not looking for.
    if bindee.identifier in ids:
        graph.add(current, bindee.identifier)

@add_edges.register(CoreBind)
def add_edges_bind(bindee, graph, current, ids):
    add_edges(bindee.bindee, graph, current, ids)

@add_edges.register(CoreCons)
def add_edges_cons(bindee, graph, current, ids):
    for param in bindee.parameters:
        add_edges(param, graph, current, ids)

@add_edges.register(CoreApplication)
def add_edges_application(bindee, graph, current, ids):
    add_edges(bindee.expr, graph, current, ids)
    add_edges(bindee.arg, graph, current, ids)

@add_edges.register(CoreLambda)
def add_edges_lambda(bindee, graph, current, ids):
    add_edges(bindee.expr, graph, current, ids)

@add_edges.register(CoreLet)
def add_edges_let(bindee, graph, current, ids):
    for local_let_bind in bindee.binds:
        add_edges(local_let_bind, graph, current, ids)
    add_edges(bindee.expr, graph, current, ids)

@add_edges.register(CoreMatch)
def add_edges_match(bindee, graph, current, ids):
    # TODO: there might be an issue here with scrutinees and binding?
    add_edges(bindee.scrutinee, graph, current, ids)
    for alt in bindee.alts:
        add_edges(alt, graph, current, ids)

@add_edges.register(CoreAlt)
def add_edges_alt(bindee, graph, current, ids):
    if bindee.expr is None: return
    add_edges(bindee.expr, graph, current, ids)

@add_edges.register(AlgebraicDataType)
def add_edges_algebraic_data_type(bindee, graph, current, ids):
    for constructor in bindee.constructors:
        add_edges(constructor, graph, current, ids)

@add_edges.register(CoreLiteral)
@add_edges.register(str) # <- builtin functions
def add_edges_noop(bindee, graph, current, ids):
    pass
