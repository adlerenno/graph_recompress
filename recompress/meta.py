from typing import List

from classes.grammar.edge import Edge
from classes.grammar.path import Path
from classes.grams.adjacency import AdjacencyType
from classes.grams.digram import DigramOccurrence, Digram
from classes.helper.dag import DAG
from classes.helper.list_dict import ListDict


class MetaGrammar:
    """This class is used to store information about a grammar object. """
    def __init__(self):
        self._meta_graphs = dict()
        self._found_occurrences = list()

    def get_meta(self, rule_name):
        try:
            return self._meta_graphs[rule_name]
        except KeyError:
            meta = MetaGraph(rule_name)
            self._meta_graphs[rule_name] = meta
            return meta

    def add_occurrence(self, pair: DigramOccurrence):
        self._found_occurrences.append(pair)

    def get_occurrences(self) -> List[DigramOccurrence]:
        return self._found_occurrences

    def clear(self):
        for meta_graph in self._meta_graphs.values():
            meta_graph.clear()
        self._found_occurrences.clear()

    def __contains__(self, item):
        return item in self._meta_graphs


class MetaGraph:
    """This class is used to store information about a graph object. """
    def __init__(self, rule_name):
        self._rule_name = rule_name
        self._node_edge_adjacency_dict = None
        self._paths = PathDict()
        self._dag = DAG(rule_name)
        self._visited = False

    def get_node_edge_adjacency_dict(self):
        return self._node_edge_adjacency_dict

    def set_node_edge_adjacency_dict(self, node_edge_adjacency_dict):
        self._node_edge_adjacency_dict = node_edge_adjacency_dict

    def add_path(self, adjacency_type: AdjacencyType, vertex, path: Path):
        self._paths.add(adjacency_type, vertex, path)  # only insertion, no replacement

    def get_paths(self):
        return self._paths

    def get_dag(self):
        return self._dag

    def clear(self):
        self._paths.clear()
        self._dag.clear()
        self._visited = False

    def is_visited(self):
        return self._visited

    def visit(self):
        self._visited = True

    def rule_changed(self):
        self.set_node_edge_adjacency_dict(None)


class PathDict:
    def __init__(self):
        """_adj maps adjacency_types to dicts, who are mapping a node to a list of paths."""
        self._adjacency_node_path_dict = dict()

    def add(self, adjacency_type: AdjacencyType, node: int, path: Path):
        if adjacency_type not in self._adjacency_node_path_dict:
            self._adjacency_node_path_dict[adjacency_type] = ListDict()
        self._adjacency_node_path_dict[adjacency_type][node] = path  # only adds, not replaces

    def add_before(self, nonterminal: Edge, position_of_nonterminal: int):
        pd = PathDict()
        for adjacency_type in self._adjacency_node_path_dict.keys():
            vertex_path_dict: ListDict = self._adjacency_node_path_dict[adjacency_type]
            for vertex in vertex_path_dict:
                paths = vertex_path_dict[vertex]
                translated_node = nonterminal[vertex]
                for path in paths:
                    pd.add(adjacency_type, translated_node, path.add_before(position_of_nonterminal, nonterminal.get_label()))
        return pd

    def get_adjacency_types(self):
        return self._adjacency_node_path_dict.keys()

    def __getitem__(self, item):
        return self._adjacency_node_path_dict[item]

    def extend(self, paths):
        for adjacency_type in paths.get_adjacency_types():
            node_path_dict = paths[adjacency_type]
            if adjacency_type not in self._adjacency_node_path_dict:
                self._adjacency_node_path_dict[adjacency_type] = ListDict()
            self._adjacency_node_path_dict[adjacency_type].extends(node_path_dict)

    def clear(self):
        self._adjacency_node_path_dict.clear()

    def __str__(self):
        return self._adjacency_node_path_dict.__str__()

    __repr__ = __str__
