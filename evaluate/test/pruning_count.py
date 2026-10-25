import unittest

from classes.grammar.edge import Edge
from classes.grammar.grammar import Grammar
from classes.grammar.graph import Graph
from classes.helper.count_dict import CountDict
from recompress.pruning import count_rules


class PruningCountTest1(unittest.TestCase):
    def setUp(self) -> None:
        self.test_grammar = Grammar(Graph([Edge('a', 0, 1), Edge('b', 1, 2), Edge(1, 2, 3, 4)]),
                                    lambda x: x in {'a', 'b'},
                                    lambda x: 2,
                                    lambda x: 3)
        self.test_grammar.add_rule(1, Graph([Edge('a', 0, 0), Edge('a', 0, 1)]))

    def test_something(self):
        result = count_rules(self.test_grammar)
        self.assertTrue(type(result) == CountDict)
        self.assertTrue(list(result.keys()) == [1])


if __name__ == '__main__':
    unittest.main()
