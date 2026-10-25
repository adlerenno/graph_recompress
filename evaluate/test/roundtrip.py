import unittest

from evaluate.timetest.average import log_average_times
from inout.input.random_graph_generator import random_grammar
from recompress import recompress, decompress


class RoundTripTestCase(unittest.TestCase):
    def test_roundtrip(self):
        g = random_grammar(50, 50, 3, ['a', 'b'], {'a': 2, 'b': 2})
        print(g)
        k = g.clone()
        decompress(k)
        print('Dekomprimierte Größe', k.size_of_hole_grammar())
        print('Ausgangsgrammatikgröße', g.size_of_hole_grammar())
        h = recompress(g)
        print('Endgrammatikgröße', h.size_of_hole_grammar())
        print(h)
        decompress(h)
        print('Dekomprimierte Größe', h.size_of_hole_grammar())
        self.assertEqual(k, h)
        log_average_times()



if __name__ == '__main__':
    unittest.main()
