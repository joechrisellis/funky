"""Useful data structures."""

from collections import defaultdict

class Scope:
    """A scope maps identifiers to arbitrary items."""

    def __init__(self, parent=None, localizer=None):
        self.local               =  {}
        self.parent              =  parent
        self.localizer           =  localizer
        self.pending_definition  =  {}

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
        return "({}, pending={}, parent={})".format(self.local, self.pending_definition, self.parent) if self.parent \
                                          else "({}, {})".format(self.local, self.pending_definition)

class Graph:
    """Graph data structure, heavily inspired by mVChr's answer on
    StackOverflow, linked below.
        https://stackoverflow.com/questions/19472530/representing-graphs-data-structure-in-python
    """

    def __init__(self, edges=[], directed=True):
        self.graph     =  defaultdict(set)
        self.directed  =  directed
        self.add_edges(edges)

    def add_node(self, node):
        self.graph[node] = set()

    def add_edges(self, edges):
        for node1, node2 in edges:
            self.add(node1, node2)

    def add(self, node1, node2):
        self.graph[node1].add(node2)
        if not self.directed:
            self.graph[node2].add(node1)

    def delete(self, node):
        for n, edges in self.graph.items():
            try:
                edges.remove(node)
            except KeyError:
                pass
        try:
            del self.graph[node]
        except KeyError:
            pass

    def is_connected(self, node1, node2):
        return node1 in self.graph and node2 in self.graph[node1]
