# from countdict import *
# from dag import *
# from digram_count import *
# from grammar import *
# from graph import *
# from pair import *
# from path import *
# from pruning_count import *
import unittest

from evaluate.test._bsp import bsp1
from recompress import recompress, decompress, MetaGrammar


class CountDictTest(unittest.TestCase):
    def setUp(self) -> None:
        self.grammar = bsp1()

    def test_something(self):
        print(self.grammar)
        meta_grammar = MetaGrammar()
        # replace_digrams(self.grammar, 0, meta_grammar)
        recompress(self.grammar)
        print(self.grammar)
        print(self.grammar.size_of_hole_grammar())
        self.grammar.clear_treat_as_terminal()
        decompress(self.grammar)
        print(self.grammar)
        print(self.grammar.size_of_hole_grammar())


def test():
    unittest.main()


if __name__ == '__main__':
    unittest.main()
