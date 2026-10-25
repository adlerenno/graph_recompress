import unittest

from classes.grammar.path import Path, PathEntry


class PathTestCase(unittest.TestCase):
    def test_something(self):
        p = Path(4, 'a')
        self.assertEqual(p[-1], PathEntry(4, 'a'))
        p1 = p.add_before(3, 'b')
        p1 = p1.add_before(2, 'b')
        p2 = p.add_before(1, 'c')
        self.assertTrue(p2 < p1)
        for symbol in p2[:-1]:
            self.assertEqual(symbol, PathEntry(1, 'c'))
        self.assertEqual(p2[-1], PathEntry(4, 'a'))


if __name__ == '__main__':
    unittest.main()
