import unittest

from classes.grammar.edge import Edge
from classes.grammar.grammar import Grammar
from classes.grammar.graph import Graph
from evaluate.test._bsp import bsp1
from recompress import replace_digrams, MetaGrammar, decompress, recompress


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.grammar = bsp1()

    def test_something(self):
        print(self.grammar)
        meta_grammar = MetaGrammar()
        # replace_digrams(self.grammar, 0, meta_grammar)
        replace_digrams(self.grammar)
        print(self.grammar)
        self.grammar.clear_treat_as_terminal()
        decompress(self.grammar)
        print(self.grammar)
        print(self.grammar.size_of_hole_grammar())


if __name__ == '__main__':
    unittest.main()
