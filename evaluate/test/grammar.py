import unittest

from classes.grammar.edge import Edge
from classes.grammar.grammar import Grammar
from classes.grammar.graph import Graph
from classes.grammar.path import Path, build_path
from classes.grams.adjacency import AdjacencyType
from classes.grams.digram import Digram
from evaluate.test._bsp import bsp1


class PathIsolationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.grammar = bsp1()
        self.digram = Digram(AdjacencyType('a', 0), AdjacencyType('b', 0))

    def test_something(self):
        self.assertEqual(self.grammar.isolate_edge(3, Path(1, 'b')), Edge('b', 2, 1))
        self.assertEqual(self.grammar.isolate_edge(3, build_path([0, 1], [4, 'b'])), Edge('b', 0, 2))
        self.assertEqual(self.grammar.isolate_edge(0, build_path([4, 0, 1], [3, 4, 'b'])), Edge('b', 2, 4))


if __name__ == '__main__':
    unittest.main()
