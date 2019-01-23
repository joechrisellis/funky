"""Implementation of Tarjan's algorithm for finding strongly connected
components in graphs.
"""

from collections import defaultdict

from funky.ds import Graph
from funky.util import get_registry_function
from funky.corelang.coretree import *

UNVISITED = -1

def reorder_bindings(bindings):
    dependency_graph = create_dependency_graph(bindings)
    sccs = find_strongly_connected_components(dependency_graph)
    visited = set()
    reordered = []

    def dfs(at):
        visited.add(at)

        neighbours = [dependency_graph.graph[x] for x in at]
        neighbours = [item for sublist in neighbours for item in sublist]

        for to in neighbours:
            scc = next(x for x in sccs if to in x)
            if scc not in visited:
                dfs(scc)
        
        reordered.append(at)

    for scc in sccs:
        if scc in visited:
            continue
        dfs(scc)

    d = {bind.identifier : bind for bind in bindings}
    reordered = [[d[b] for b in g] for g in reordered]

    return reordered

def create_dependency_graph(bindings):
    """Given a collecion of CoreBinds, creates a graph representing how the
    bindings depend on one another. For instance, in:

        a = b 10
        b x = x + 1
        c = a
    
    a depends on b, b depends on nothing, and c depends on a.
    """

    graph = Graph()

    ids = [bind.identifier for bind in bindings]
    for bind in bindings:
        graph.add_node(bind.identifier)
        add_edges(bind.bindee, graph, bind.identifier, ids)

    return graph

def find_strongly_connected_components(graph):
    """Applies Tarjan's algorithm to split a graph down into its strongly
    connected components. We use this in the compiler to 'sort' bindings
    in a core let statement.
    """
    # TODO: document this better

    i = scc_count = 0
    ids, low = defaultdict(lambda: UNVISITED), defaultdict(lambda: 0)
    on_stack = defaultdict(lambda: False)
    stack = []
    
    def dfs(at):
        nonlocal i, scc_count
        stack.append(at)
        on_stack[at] = True
        i += 1
        ids[at] = low[at] = i

        # visit all neighbours and minimise lowlink on callback
        for to in graph.graph[at]:
            if ids[to] == UNVISITED:
                dfs(to)
            if(on_stack[to]):
                low[at] = min(low[at], low[to])

        # once we've visited all neighbours of 'at', if we're at the start of a
        # strongly connected component empty the seen stack until we're back to
        # the start of the component.
        if ids[at] == low[at]:
            while stack:
                node = stack.pop()
                on_stack[node] = False
                low[node] = ids[at]
                if node == at: break
            scc_count += 1

    for node in graph.graph:
        if ids[node] != UNVISITED: continue
        dfs(node)

    reversed_dict = defaultdict(list)
    for k, v in low.items():
        reversed_dict[v].append(k)

    strongly_connected_components = [tuple(l) for l in reversed_dict.values()]
    return strongly_connected_components

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
    for alt in bindee.alts:
        add_edges(alt, graph, current, ids)

@add_edges.register(CoreAlt)
def add_edges_alt(bindee, graph, current, ids):
    if bindee.expr is None: return
    add_edges(bindee.expr, graph, current, ids)

@add_edges.register(CoreLiteral)
@add_edges.register(str) # <- builtin functions
def add_edges_noop(bindee, graph, current, ids):
    pass
