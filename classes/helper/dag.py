from typing import List, Any

from classes.grammar.path import Path
from evaluate.timetest.average import average_timing


class DAGNode:

    def __init__(self, name, path_end: int = None):
        self._name = name
        self._path_ends = list()
        if path_end is not None:
            self.add_path_end(path_end)
        self._next_nodes = dict()

        self._new_rule_name = None

        self._parents = list()

    def add_path_end(self, path_end: int):
        self._path_ends.append(path_end)

    def has_path_end(self, path_end: int):
        return path_end in self._path_ends

    def get_path_ends(self):
        return self._path_ends

    def set_next(self, path_symbol, next_node):
        self._next_nodes[path_symbol] = next_node

    def get_next(self, path_symbol):
        return self._next_nodes[path_symbol]

    def get_next_positions(self):
        return self._next_nodes.keys()

    def get_name(self) -> int:
        """Returns the name of the old rule."""
        return self._name

    def get_new_name(self):
        return self._new_rule_name

    def set_new_name(self, new_name):
        """Used to store a new Name for a rule."""
        self._new_rule_name = new_name

    def equals(self, other):
        if type(other) is not DAGNode:
            return False
        else:
            other_dag_node: DAGNode = other
            return self.get_name() == other_dag_node.get_name() \
                and self._next_nodes == other_dag_node._next_nodes \
                and set(self._path_ends) == set(other_dag_node._path_ends)

    def __hash__(self):
        return self.__str__().__hash__()

    def __str__(self):
        return f'({self._name}, {self._new_rule_name}, ends={self._path_ends}, next_keys={list(self._next_nodes.keys())})'

    __repr__ = __str__

    def _add_parent(self, node, path_symbol):
        """only used by _MultiHeadDAG"""
        self._parents.append((node, path_symbol))

    def _get_parents(self):
        return self._parents

    def _clear_parents(self):
        self._parents.clear()

    def update_path_symbols(self, affected_positions: list):
        """e.g. if there were the symbols 1, 3, 7 before, the affected position list would habe to be
        [1, 3, 7] and then, it would be 0, 1, 2 (index from [1, 3, 7])"""
        self._path_ends = [affected_positions.index(path_end) for path_end in self._path_ends]
        self._next_nodes = {affected_positions.index(key): node for key, node in self._next_nodes.items()}


class DAG:
    def __init__(self, head_name: int):
        self._head = DAGNode(head_name)

    def has_path(self, path: Path) -> bool:
        node: DAGNode = self._head
        for path_entry in path[:-1]:
            path_position = path_entry.position
            try:
                node = node.get_next(path_position)
            except KeyError:
                return False
        return node.has_path_end(path[-1].position)

    def add_path(self, path: Path):
        node: DAGNode = self._head
        for path_entry in path[:-1]:
            path_position = path_entry.position
            try:
                node = node.get_next(path_position)
            except KeyError:
                next_node = DAGNode(name=path_entry.label)
                node.set_next(path_position, next_node)
                node = next_node
        node.add_path_end(path[-1].position)

    def add_sub_dag(self, path: Path, sub_dag):
        node: DAGNode = self._head
        for path_entry in path[:-1]:
            path_position = path_entry.position
            try:
                node = node.get_next(path_position)
            except KeyError:
                next_node = DAGNode(name=path_entry.label)
                node.set_next(path_position, next_node)
                node = next_node
        node.set_next(path[-1].position, sub_dag._head)

    @average_timing
    def minimize(self):
        """Method used to find equal nodes and transform the tree of nodes to a dag."""
        # equality depends on how long the path to childs are.
        # leaves have no childs, so they can possibly be equal and the start_point
        _leaves = list()

        # temporary node-store for visiting
        nodes_to_visit = [self._head]
        while not len(nodes_to_visit) == 0:
            node = nodes_to_visit.pop(0)

            # store leave
            if len(node.get_next_positions()) is 0:
                _leaves.append(node)

            # all nodes must be visited. ensure backward traversal
            for next_position in node.get_next_positions():
                next_node: DAGNode = node.get_next(next_position)
                nodes_to_visit.append(next_node)

                # for backward traversal the parents must be known.
                next_node._add_parent(node, next_position)
        # end prepare, start equality check

        # a generation are all nodes of the same max-path-to-child-length. There cannot be other equal nodes.
        # generation are visited from the leaves to the head.
        generation = _leaves
        next_generation = list()
        while len(generation) is not 0:
            i, j = 0, 1
            while i < len(generation):
                gen_i = generation[i]
                while j < len(generation):
                    new_next_node = generation[j]

                    # compare two nodes on equality
                    if gen_i.equals(new_next_node):
                        # unify the nodes by change parent pointers and remove deleted from generation list.
                        for parent, path_symbol in new_next_node._get_parents():
                            parent.set_next(path_symbol, gen_i)
                            if parent not in next_generation:
                                next_generation.append(parent)
                        del generation[j]
                    else:
                        # ensure next one is tested
                        j += 1
                # ensure next one is tested
                i += 1
                j = i + 1

                # build next_generation, remove parents.
                for node, path_symbol in gen_i._get_parents():
                    if node not in next_generation:
                        next_generation.append(node)
                gen_i._clear_parents()

            # generation change
            generation = next_generation
            next_generation = list()
        # end minimize

    @average_timing
    def get_nodes(self) -> List[DAGNode]:
        ret = {self._head}
        nodes_to_visit = [self._head]
        while not len(nodes_to_visit) == 0:
            node = nodes_to_visit.pop(0)
            for next_position in node.get_next_positions():
                ret.add(node.get_next(next_position))
                nodes_to_visit.append(node.get_next(next_position))
        return list(ret)

    def get_nodes_except_head(self) -> List[DAGNode]:
        nodes = self.get_nodes()
        del nodes[nodes.index(self._head)]
        return nodes

    def get_head(self) -> DAGNode:
        return self._head

    def clear(self):
        self._head = DAGNode(self._head.get_name())

    def is_empty(self) -> bool:
        return len(self._head.get_next_positions()) is 0 and len(self._head.get_path_ends()) is 0

    @average_timing
    def deep_copy(self):
        """TODO: Objektidentität nicht erhalten bisher. Erzeugt Baum"""
        copied = DAG(self._head.get_name())
        nodes_to_copy_state = [(self._head, copied._head)]
        while not len(nodes_to_copy_state) == 0:
            node_old, node_new = nodes_to_copy_state.pop(0)
            for end_path in node_old.get_path_ends():
                node_new.add_path_end(end_path)
            for next_position in node_old.get_next_positions():
                next_node = node_old.get_next(next_position)
                next_node_new = DAGNode(next_node.get_name())
                nodes_to_copy_state.append((next_node, next_node_new))
                node_new.set_next(next_position, next_node_new)
        return copied
