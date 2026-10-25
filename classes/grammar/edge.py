class Edge:
    def __init__(self, label, *args, nodes=None):
        """Inits an labeled Hyperedge.
        :param label: label of the new edge.
        :param args: all following arguments are treated as vertices."""
        self._label = label
        self._nodes = args if nodes is None else nodes
        self._nodes = tuple(self._nodes)
        self._mark_as_delete = False

    def __repr__(self):
        """:returns a String representation of this edge object."""
        return "('{}', {})".format(self._label, ", ".join((str(n) for n in self._nodes)))

    __str__ = __repr__

    def __len__(self):
        """:returns the number of nodes attached to this edge. Should always me the same result as edge.rank()"""
        return len(self._nodes)

    def __getitem__(self, item):
        """:returns the node with connection_type 'item'"""
        if item >= len(self._nodes):
            raise KeyError(f'Edge {self} has no vertex at connection type {item}.')
        return self._nodes[item]

    def __iter__(self):
        """:returns an iterable looping over the attached nodes in order of their connection_types."""
        return self._nodes.__iter__()

    def get_nodes(self):
        """:returns a list of the attached nodes ordered after the connection_type."""
        return self._nodes

    def get_label(self):
        """:returns the label of this edge."""
        return self._label

    def rank(self):
        """:returns the rank of this edge"""
        return len(self._nodes)

    def is_hyperedge(self):
        """Method to determine, if an edge is a hyperedge. Used only by latex.py"""
        return len(self._nodes) != 2

    def is_loop(self):
        """Method to determine, if an edge is normal and only connected to one node. Used only by latex.py"""
        return self.rank() is 2 and len(set(self._nodes)) is 1

    def size_of(self):
        """:returns the size to save this edge. +1 is for the label of the Edge. """
        return self.rank() + 1

    def __eq__(self, other):
        """:returns true if and only if self and other represent the same edge."""
        return self._label == other.get_label() and self._nodes == other.get_nodes()

    def change_label(self, new_label):
        self._label = new_label

    def clone(self):
        return Edge(self._label, nodes=self._nodes)

    def mark_as_delete(self):
        self._mark_as_delete = True

    def is_mark_as_delete(self):
        return self._mark_as_delete
