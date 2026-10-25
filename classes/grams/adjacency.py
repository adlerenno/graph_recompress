from classes.grammar.edge import Edge


class AdjacencyType(tuple):
    def __new__(cls, label, connection_type):
        """Fixes an AdjacencyType to a label and an connection_type

        :param label: Label of the adjacency type. Can be anything hashable.
        :param connection_type: A connection type is a natural number (with 0). It must fit to the rank of the label."""
        return tuple.__new__(AdjacencyType, (label, connection_type))

    def get_label(self):
        """:returns the label of this AdjacencyType."""
        return self[0]

    def get_connection_type(self):
        """:returns the connection type of this AdjacencyType."""
        return self[1]

    def fit_to_edge(self, edge: Edge):
        return self.get_label() == edge.get_label()
