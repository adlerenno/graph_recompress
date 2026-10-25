import unittest

from classes.grammar.path import Path, build_path
from classes.helper.dag import DAG


class DagTestCase(unittest.TestCase):
    def test_something(self):
        dag = DAG('A')
        self.assertTrue(not dag.has_path(Path(3, 'B')))
        dag.add_path(Path(3, 'B'))
        self.assertTrue(dag.has_path(Path(3, 'B')))
        p = Path(3, 'B').add_before(2, 'D').add_before(1, 'E')
        dag.add_path(p)
        self.assertTrue(dag.has_path(p))
        p = Path(2, 'B').add_before(2, 'D').add_before(1, 'E')
        self.assertTrue(not dag.has_path(p))


class DagMinimizeTestCase(unittest.TestCase):
    def test_1(self):
        paths = [build_path([0, 0, 0], [1, 2, 'a']),
                 build_path([0, 1, 0], [1, 2, 'a'])]
        dag = DAG('A')
        for path in paths:
            dag.add_path(path)
        dag.minimize()
        self.assertEqual(dag._head.get_next(0).get_next(0), dag._head.get_next(0).get_next(1))

    def test_2(self):
        paths = [build_path([0, 0, 0], [1, 2, 'a']),
                 build_path([0, 1, 0], [1, 2, 'a']),
                 build_path([0, 0, 0, 1, 0], [1, 2, 3, 4, 'a']),
                 build_path([0, 1, 0, 1, 0], [1, 2, 3, 4, 'a'])
                 ]
        dag = DAG('A')
        for path in paths:
            dag.add_path(path)
        dag.minimize()
        # list(map(print, dag.get_nodes()))
        self.assertEqual(dag._head.get_next(0).get_next(0), dag._head.get_next(0).get_next(1))
        # print('after')
        # list(map(print, dag.get_nodes()))


if __name__ == '__main__':
    unittest.main()
