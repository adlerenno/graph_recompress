import unittest

from classes.grammar.edge import Edge
from classes.grammar.grammar import Grammar
from classes.grammar.graph import Graph
from classes.grammar.path import Path, build_path
from classes.grams.adjacency import AdjacencyType
from classes.grams.digram import Digram, DigramOccurrence
from classes.helper.count_dict import CountDict
from evaluate.test._bsp import bsp1
from recompress.digrams import count_digrams, build_occurrences, find_all_occurrences_of_digram
from recompress.meta import MetaGraph, MetaGrammar


class DigramCount(unittest.TestCase):
    def setUp(self) -> None:
        self.grammar = bsp1()
        self.digram = Digram(AdjacencyType('a', 0), AdjacencyType('b', 0))

    def testCountDigrams(self):
        cd = CountDict()
        cd[Digram(AdjacencyType('a', 0), AdjacencyType('a', 1))] = 5
        cd[Digram(AdjacencyType('a', 0), AdjacencyType('b', 0))] = 8
        cd[Digram(AdjacencyType('a', 0), AdjacencyType('b', 1))] = 5
        cd[Digram(AdjacencyType('a', 0), AdjacencyType('a', 0))] = 3
        cd[Digram(AdjacencyType('a', 1), AdjacencyType('b', 0))] = 5
        cd[Digram(AdjacencyType('a', 1), AdjacencyType('b', 1))] = 8
        cd[Digram(AdjacencyType('b', 0), AdjacencyType('b', 1))] = 5
        cd[Digram(AdjacencyType('b', 0), AdjacencyType('b', 0))] = 3
        cd[Digram(AdjacencyType('a', 1), AdjacencyType('a', 1))] = 2
        cd[Digram(AdjacencyType('b', 1), AdjacencyType('b', 1))] = 2
        meta_grammar = MetaGrammar()
        result = count_digrams(self.grammar, meta_grammar, 0)
        self.assertDictEqual(dict(result), dict(cd))
        # for key in result:
        #     print(key, ': ', result[key])

    def testFindOccurrences(self):
        meta = MetaGrammar()
        print(find_all_occurrences_of_digram(self.grammar, 0, Digram(AdjacencyType('a', 0), AdjacencyType('b', 0)), meta))
        print(4, meta.get_meta(4).get_paths())
        print(3, meta.get_meta(3).get_paths())
        print(2, meta.get_meta(2).get_paths())
        print(1, meta.get_meta(1).get_paths())
        print(0, meta.get_meta(0).get_paths())
        print('occurrences', meta.get_occurrences())


class DigramBuild(unittest.TestCase):
    def setUp(self) -> None:
        self.digram = Digram(AdjacencyType('a', 0), AdjacencyType('a', 1))
        self.meta_grammar: MetaGrammar = MetaGrammar()
        self.meta: MetaGraph = self.meta_grammar.get_meta('A')
        self.meta.add_path(AdjacencyType('a', 0), 1, Path(3, 'D'))
        self.meta.add_path(AdjacencyType('a', 0), 1, Path(4, 'E'))
        self.meta.add_path(AdjacencyType('a', 1), 1, Path(3, 'D'))
        self.meta.add_path(AdjacencyType('a', 1), 1, Path(5, 'F'))

        self.meta.add_path(AdjacencyType('a', 1), 2, Path(5, 'F'))
        self.meta.add_path(AdjacencyType('a', 0), 2, Path(6, 'G'))
        self.meta.add_path(AdjacencyType('a', 1), 2, Path(1, 'B'))

    def testBuildDigrams(self):
        build_occurrences(self.digram, self.meta, self.meta_grammar, 'A')
        pair0: DigramOccurrence = self.meta_grammar.get_occurrences()[0]
        self.assertEqual(pair0.get_path_to_adjacency_type_0(), Path(3, 'D'))
        self.assertEqual(pair0.get_path_to_adjacency_type_1(), Path(5, 'F'))
        pair1 = self.meta_grammar.get_occurrences()[1]
        self.assertEqual(pair1.get_path_to_adjacency_type_0(), Path(6, 'G'))
        self.assertEqual(pair1.get_path_to_adjacency_type_1(), Path(1, 'B'))


class DigramFindOccurrences(unittest.TestCase):
    def setUp(self) -> None:
        s = Graph([Edge(1, 0, 1, 2), Edge('b', 0, 2)], rank=5)
        a = Graph([Edge(2, 0, 1, 2), Edge(3, 0, 1, 2)], rank=3)
        b = Graph([Edge('a', 0, 1), Edge('a', 0, 2)], rank=3)
        c = Graph([Edge('b', 0, 1), Edge('b', 1, 2)], rank=3)
        self.grammar = Grammar(s, lambda x: x in {'a', 'b'}, lambda x: 2, lambda x: 3)
        self.grammar.add_rule(1, a)
        self.grammar.add_rule(2, b)
        self.grammar.add_rule(3, c)
        self.digram = Digram(AdjacencyType('a', 0), AdjacencyType('b', 0))

    def testCountDigrams(self):
        meta = MetaGrammar()
        paths, dag = find_all_occurrences_of_digram(self.grammar, 0, self.digram, meta)
        pairs = meta.get_occurrences()
        self.assertIn(DigramOccurrence(self.digram, build_path([0, 0], [2, 'a']), build_path([1, 0], [3, 'b']), 1), pairs)
        self.assertIn(DigramOccurrence(self.digram, build_path([0, 0, 1], [1, 2, 'a']), build_path([1], ['b']), 0), pairs)


if __name__ == '__main__':
    unittest.main()
