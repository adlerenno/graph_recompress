from classes.grams.adjacency import AdjacencyType
from classes.helper.count_dict import CountDict, AutoAddCountDict
from evaluate.timetest.average import average_timing


class Graph:
    def __init__(self, edges: list = None, rank: int = -1):
        """Inits a Graph object.
        :param: edges: initial edges of this graph.
        :param: rank: rank is the rank of the edge used to represent this rule.
        It's equal to the number of nodes in this graph.
        It's optional to use this field."""
        self._edges = [] if edges is None else edges
        self._rank = rank

        self._node_edge_adjacency_dict = None

    def __iadd__(self, new_edge):
        """Used to add an edge to the Graph
        :param new_edge: the new edge."""
        self._edges += [new_edge]
        return self

    __add__ = __iadd__

    def get_edges(self):
        """:returns all edges within this graph object."""
        return self._edges

    def __getitem__(self, id):
        """:returns the edge at a given ID"""
        return self._edges[id]

    def __setitem__(self, id, new_edge):
        """Replaces a new edge at the given ID.
        :param id: id of the edge.
        :param new_edge: the new edge"""
        self._edges[id] = new_edge

    def __delitem__(self, id):
        """Deletes an edge at a given ID.
        :param id: id of the edge, which is going to be deleted."""
        del self._edges[id]

    def __str__(self):
        """:returns a string representation of the this graph."""
        return "Graph {}".format(self._edges)

    __repr__ = __str__

    def __len__(self):
        """:returns the number of edges within the graph."""
        return len(self._edges)

    def size_of(self):
        """:returns: the cumulative size of all rules."""
        return sum((e.size_of() for e in self._edges))

    def __iter__(self):
        """:returns an iterable over the edges. Used for loops"""
        return self._edges.__iter__()

    def rank(self):
        """:returns: the rank field.
        Can be interpreted as the node count or as the rank of the non-terminal edges representing this rule."""
        return self._rank

    def extend(self, edges):
        """Adds the edges to this graph.
        :param edges: iterable over the new to add edges."""
        self._edges.extend(edges)

    def __eq__(self, other):
        """:returns true, if and only if both graphs are equal. The order of the edges is not important."""
        edges = self.get_edges().copy()
        for e in other.get_edges():
            edges.remove(e)
        return len(edges) == 0

    @average_timing
    def clone(self):
        return Graph(edges=[edge.clone() for edge in self._edges], rank=self.rank())

    @average_timing
    def get_node_edge_adjacency_dict(self) -> AutoAddCountDict:
        """Returns a dict. At index i, it contains a dict mapping an AdjacencyType to its frequency at the node i"""

        # Simply loop over all edges and all nodes a build the mapping of nodes to AdjacencyTypes.
        node_edge_adjacency_dict = AutoAddCountDict()
        for edge in self:
            for connection_type in range(edge.rank()):
                adjacency_type = AdjacencyType(edge.get_label(), connection_type)
                node = edge[connection_type]
                # Update process. Used to generate objects if they are not available. Done by AutoAddCountDict
                node_edge_adjacency_dict[node][adjacency_type] += 1
        return node_edge_adjacency_dict
