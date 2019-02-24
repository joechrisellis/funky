"""Implementation of Tarjan's algorithm for finding strongly connected
components in graphs.
"""

import logging

from collections import defaultdict

from funky.corelang.coretree import *

log = logging.getLogger(__name__)

UNVISITED = -1

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
