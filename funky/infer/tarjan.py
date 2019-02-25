"""Implementation of Tarjan's algorithm for finding strongly connected
components in graphs.
"""

import logging
from collections import defaultdict

log = logging.getLogger(__name__)

UNVISITED = -1

def reorder_bindings(corelet_node):
    """Reorders the given bindings by dependencies. Keeps mutually-dependent
    groups together.
    
    :param bindings: a list of bindings
    :return:         the bindings, sorted in reverse dependency order
    :rtype:          list
    """
    dependency_graph = corelet_node.dependency_graph
    
    log.debug("Reordering {} bindings...".format(len(corelet_node.binds)))

    log.debug("Finding strongly-connected components within dependency graph...")
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

    d = {bind.identifier : bind for bind in corelet_node.binds}
    reordered = [[d[b] for b in g] for g in reordered]

    log.debug("Finished reordering bindings.")
    return reordered

def find_strongly_connected_components(graph):
    """Applies Tarjan's algorithm to split a graph down into its strongly
    connected components. We use this in the compiler to 'sort' bindings
    in a core let statement.

    :param graph: a dependency graph
    :return:      a list of strongly connected components
    :rtype:       list
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
