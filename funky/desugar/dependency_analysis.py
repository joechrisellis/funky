import logging

from funky.corelang.coretree import *
from funky.corelang.types import AlgebraicDataType
from funky.ds import Graph
from funky.util import get_registry_function

log = logging.getLogger(__name__)

def prune_bindings(bindings, dependency_graph, tmp_varname):
    """Prunes the core tree by getting rid of any unused bindings."""
    keep, visited = set(), set()

    def dfs(at):
        visited.add(at)
        neighbours = dependency_graph.graph[at]
        for to in neighbours:
            if to not in visited:
                dfs(to)
        keep.add(at)

    dfs(tmp_varname) # <- populate our 'keep' variable

    # get rid of any unused bindings, as well as our temporary binding
    new_bindings = [b for b in bindings if b.identifier in keep and \
                                        not b.identifier == tmp_varname]
    return new_bindings

def create_dependency_graph(bindings):
    """Given a collecion of CoreBinds, creates a graph representing how the
    bindings depend on one another. For instance, in:

        a = b 10
        b x = x + 1
        c = a
    
    a depends on b, b depends on nothing, and c depends on a.

    :param bindings: the bindings
    :return:         a graph object representing the dependencies
    :rtype:          Graph
    """

    graph = Graph()

    ids = [bind.identifier for bind in bindings]
    for bind in bindings:
        graph.add_node(bind.identifier)
        add_edges(bind.bindee, graph, bind.identifier, ids)

    return graph

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
    # recursively perform dependency analysis to prune this CoreLet
    do_dependency_analysis(bindee)
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

def prune_unused_bindings(core_tree):
    tmp_varname = "_let_expr"
    let_expr = CoreBind(tmp_varname, core_tree.expr)
    bindings = [*core_tree.binds, let_expr]
    dependency_graph = create_dependency_graph(bindings)

    pruned_bindings = prune_bindings(bindings, dependency_graph, tmp_varname)
    core_tree.binds = pruned_bindings

def do_dependency_analysis(core_tree):
    prune_unused_bindings(core_tree)
