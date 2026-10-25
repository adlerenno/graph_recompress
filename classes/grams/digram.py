from functools import reduce

from classes.grammar.edge import Edge
from classes.grammar.graph import Graph
from classes.grammar.path import Path
from evaluate.timetest.average import average_timing_name


class Digram(tuple):
    """This class is used to represent a Digram. Note, that the order of the AdjacencyTypes is important when comparing,
    but it is not important within the graph-repair-algorithm."""

    def __new__(cls, adjacency_type_1, adjacency_type_2):
        """Fixes a Digram to two AdjacencyTypes.
        :param adjacency_type_1: first AdjacencyType.
        :param adjacency_type_2: second Adjacency Type."""
        return tuple.__new__(Digram, (adjacency_type_1, adjacency_type_2))

    def invert(self):
        """:returns a Digram with the AdjacencyTypes in inverted order."""
        return Digram(self[1], self[0])

    def get_other(self, adjacency_type):
        """:returns the other adjacency_type which is not given. If the Digram has two times the same AdjacencyType,
        it returns an equal as given, but not the same (no Object identity)"""
        return self[1] if self[0] == adjacency_type else self[0]

    # def __eq__(self, other):
    #    return super().__eq__(other) or (self[0] == other[1] and self[1] == other[0])

    # def __hash__(self):
    #    return super().__hash__()

    # def __str__(self):
    #    return 'Digram {}'.format(super().__str__())

    # repr__ = __str__

    def set_rule_name(self, name):
        self.rule_name = name

    """This class is used as a creator for the new Rule from a digram and to replace
    two edges by a new hyperedge with correct order of nodes."""
    @average_timing_name('create_new_digram_rule')
    def create_rule(self, grammar):
        """ Constructs the class as well as the new rule object (instance of class graph)

        :param digram: Should be of type Digram.
        :param grammar: Should be the grammar object where the digram is replaced.
        """

        def build_edge(label, connection_type, rank_of_rule, node_offset):
            """Help method to create one of the edges used within the new rule of a digram
            :param label: the label of the returned edge
            :param connection_type: the node 0 will have this connection_type.
            :param rank_of_rule: rank of the new created rule.
            :param node_offset: Used to shift all node ids. Should not be 0!
            :returns one edge that will be used in the rule."""
            nodes = list(range(node_offset, rank_of_rule + node_offset - 1))
            nodes.insert(connection_type, 0)
            return Edge(label, *nodes)

        label = [self[i].get_label() for i in range(len(self))]
        rank = [grammar.rank_of_rule(rule_name) for rule_name in label]
        edges = [build_edge(label[0], self[0].get_connection_type(), rank[0], 1),
                 build_edge(label[1], self[1].get_connection_type(), rank[1], rank[0])]
        return Graph(edges, rank[0] + rank[1] - 1)

    @average_timing_name('apply_digram_to_edges')
    def apply_to_edges(self, *edges):
        """Creates a hyperedge for the two edges after the ruling to the represented Rule.
        Note that the order of edge_1 and edge_2 must be given as it fits to the digram.

        :param edges: Catches up every position argument. Should be exactly two edges.
        :returns a non-terminal describing the given edges."""
        nodes = list(map(lambda e: list(e.get_nodes()), edges))

        shared_node = nodes[0][self[0][1]]

        def delete_shared_node(l, position):
            del l[position]
            return l
        nodes = map(lambda x: delete_shared_node(x[0], x[1][1]), zip(nodes, self))
        return Edge(self.rule_name, shared_node, *list(reduce(lambda x, y: x+y, nodes)))


class DigramOccurrence:
    def __init__(self, digram, path1, path2, occurring_rule_name):
        self._digram = digram
        self._path0 = path1
        self._path1 = path2
        self._occurring_rule_name = occurring_rule_name
        #  used to store Edges which are already isolated but not used yet.
        self._edge0 = None
        self._edge1 = None

    def get_path_to_adjacency_type_0(self):
        return self._path0

    def get_path_to_adjacency_type_1(self):
        return self._path1

    def get_occurring_rule_name(self):
        return self._occurring_rule_name

    def __str__(self):
        return f'{self._digram} -> {self._occurring_rule_name} - {self._path0} + {self._path1}'

    __repr__ = __str__

    def __eq__(self, other):
        other: DigramOccurrence = other
        return self._digram == other._digram and self._path0 == other._path0 and self._path1 == other._path1 and self._occurring_rule_name == other._occurring_rule_name \
               or self._digram == other._digram.invert() and self._path1 == other._path0 and self._path0 == other._path1 and self._occurring_rule_name == other._occurring_rule_name

