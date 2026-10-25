from classes.grammar.edge import Edge
from classes.grammar.graph import Graph
from evaluate.timetest.average import average_timing_name


class Monogram(tuple):
    def __new__(cls, label, connection_type_1, connection_type_2):
        """Fixes a Monogram to a label and two connection_types

        :param label: Label of the monogram
        :param connection_type_1: Should be the lower connection_type. A connection type is simply a number.
        :param connection_type_2: Should be the higher connection_type. A connection type is simply a number.
        connection_type_2 must be different from connection_type_1!"""
        return tuple.__new__(Monogram, (label, connection_type_1, connection_type_2))

    def get_label(self):
        """:returns the label of the Monogram."""
        return self[0]

    def set_rule_name(self, name):
        self._rule_name = name

    def get_rule_name(self):
        return self._rule_name

    @average_timing_name('create_new_monogram_rule')
    def create_rule(self, grammar):
        """Constructs the new rule.
        :param grammar: Should be the grammar, where the Monogram should be applied to.
        """

        def build_edge(label, connection_type_1, connection_type_2, rank_of_rule, node_offset):
            """Help method to create the edge used within the new rule of a monogram
            :param label: the label of the returned edge
            :param connection_type_1: this type should be repeated.
            :param connection_type_2: this characterizes the position of the repetition.
            :param rank_of_rule: rank of the new created rule.
            :param node_offset: Used to shift all node ids. Should be 0 to use minimal ids.
            :returns the edge that will be used in the rule."""
            nodes = list(range(node_offset, rank_of_rule + node_offset - 1))
            nodes.insert(connection_type_2, nodes[connection_type_1])
            return Edge(label, *nodes)
        rank = grammar.rank_of_rule(self.get_label())
        edges = [build_edge(self.get_label(), self[1], self[2], rank, 0)]
        return Graph(edges, rank - 1)

    @average_timing_name('apply_monogram_to_edge')
    def apply_to_edge(self, edge):
        """Creates a hyperedge for the edge corresponding to the monogram given while creating this object.
        :returns an edge object without the monogram[2] node.

        :param edge: edge where the given monogram can applied to (no check within). """
        nodes = list(edge.get_nodes())
        del nodes[self[2]]
        return Edge(self.get_rule_name(), *nodes)
