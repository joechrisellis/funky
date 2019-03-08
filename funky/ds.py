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
        
        :param item: the item in question.
        :return:     the corresponding dict item if found, None otherwise
        :rtype:      dict or None
        """
        return self.local.get(item)

    def rsearch(self, item):
        """Recursively searches the scope for an item. First checks if the item
        is in this scope, then recursively searches the parent scope to see if
        it is defined at a higher level.

        :param item: the item in question
        :return:     the corresponding dict item if found, None otherwise
        :rtype:      dict or None
        """
        if item in self.local:
            return self.local[item]
        elif self.parent:
            return self.parent.rsearch(item)
        else:
            return None

    def get_pending_name(self, key):
        """Gets the pending name for a particular key.
        
        :param key str: the name of the pending definition
        :return:        the placeholder name, if there is one, otherwise None
        """
        try:
            return self.pending_definition[key]
        except KeyError:
            if self.parent:
                return self.parent.get_pending_name(key)
            else:
                return None

    def is_pending_definition(self, key):
        """Returns True if the given key is pending definition, False
        otherwise. If the key is not found in the local scope, this method
        delegates to the parent's scope to check there.
        
        :param key str: the name to check
        :return:        True if the given key is pending a definition, False
                        otherwise
        :rtype          bool
        """
        if key in self.pending_definition:
            return True
        if self.parent:
            return self.parent.is_pending_definition(key)
        return False

    def __getitem__(self, key):
        """Recursively searches the scope for a given key and returns it.

        :param key: the key to search
        :return:    the corresponding data in the scope
        """
        return self.rsearch(key)

    def __setitem__(self, key, value):
        """Sets an item in the local scope dict.

        :param key:   the key of the item
        :param value: any auxiliary data you want to add
        """
        self.local[key] = value

    def __contains__(self, item):
        """A scope 'contains' an item (in other words, that item is defined)
        if it can be found with a recursive search.

        :param item: the item in question
        :return:     True if the item is defined in the scope, False otherwise
        :rtype:      bool
        """
        return self.rsearch(item) is not None

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
        """Add a node to the graph.
        
        :param node: the label for the new node
        """
        if node not in self.graph:
            self.graph[node] = set()

    def add_edges(self, edges):
        """Add some edges between two nodes in the graph.
        
        :param edges list: the list of edges
        """
        for node1, node2 in edges:
            self.add(node1, node2)

    def add(self, node1, node2):
        """Add a single edge between two nodes in the graph. If the graph is
        not directed, add the edge in both directions.
        
        :param node1: the 'from' node
        :param node2: the 'to' node
        """
        self.graph[node1].add(node2)
        if not self.directed:
            self.graph[node2].add(node1)

    def delete(self, node):
        """Removes a node entirely from the graph, including any edges
        referring to it.
        
        :param node: the node to remove
        """
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
        """Checks if two nodes are connected.
        
        :param   node1: the 'from' node
        :param   node2: the 'to' node
        :return: True if node1 has an edge to node2, False otherwise
        :rtype:  bool
        """
        return node1 in self.graph and node2 in self.graph[node1]

    def __str__(self):
        return str(self.graph)
