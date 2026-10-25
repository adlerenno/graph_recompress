from classes.grammar.edge import Edge
from classes.grammar.grammar import Grammar
from classes.grammar.graph import Graph
from evaluate.timetest.average import average_timing_name


class Nogram(tuple):
    def __new__(cls, label, use_vector):
        """Fixes a nogram to a label and an use_vector.

        :param label: Label of the adjacency type. Can be anything hashable.
        :param use_vector: """
        return tuple.__new__(Nogram, (label, use_vector))

    def get_label(self):
        """:returns the label of this nogram."""
        return self[0]

    def get_use_vector(self):
        """:returns the use_vector of this nogram."""
        return self[1]

    def should_replace(self) -> bool:
        """Checks whether at least one node is not needed."""
        return not self.get_use_vector().are_all_true()

    @average_timing_name('nogram_by_rule')
    def by_rule(self, grammar: Grammar):
        """Updates this nogram to the current Version of the grammar rule by the label of this nogram.
        Modifies the use_vector."""
        use_vector = self.get_use_vector()
        use_vector.all_false()
        rule = grammar[self.get_label()]
        for edge in rule:
            for node in edge.get_nodes():
                use_vector[node] = True

    @average_timing_name('create_new_nogram_rule')
    def create_rule(self, grammar: Grammar) -> Graph:
        """:returns a Graph objekt representing the grammar rule after the replacement of this nogram."""
        rule = grammar[self.get_label()]
        new_edges = []
        use_vector = self.get_use_vector()
        for edge in rule:
            new_edges.append(Edge(edge.get_label(), nodes=[use_vector.rank(node) for node in edge]))
        return Graph(edges=new_edges, rank=use_vector.get_max_rank())

    @average_timing_name('apply_nogram_to_edge')
    def apply_to_edge(self, edge: Edge) -> Edge:
        """:returns an edge, where this nogram is applied to. Changes the nodes of the edge only."""
        return Edge(edge.get_label(), nodes=[node for i, node in enumerate(edge.get_nodes())
                                             if self.get_use_vector()[i]])
