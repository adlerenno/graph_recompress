import unittest

from classes.grammar.edge import Edge
from classes.grammar.graph import Graph
from classes.helper.count_dict import AutoAddCountDict


class GetNodeEdgeAdjacencyDictTest(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = Graph([Edge('a', 0, 1), Edge(1, 0, 1, 2, 0)])

    def test_something(self):
        compare_value = AutoAddCountDict()
        compare_value[0][('a', 0)] += 1
        compare_value[1][('a', 1)] += 1
        compare_value[0][(1, 0)] += 1
        compare_value[1][(1, 1)] += 1
        compare_value[2][(1, 2)] += 1
        compare_value[0][(1, 3)] += 1
        self.assertEqual(self.graph.get_node_edge_adjacency_dict(), compare_value)


if __name__ == '__main__':
    # print(Graph([Edge('a', 0, 1), Edge(1, 2, 3, 4, 5)]).get_node_edge_adjacency_dict)
    unittest.main()
