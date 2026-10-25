import unittest

from classes.helper.count_dict import CountDict, AutoAddCountDict


class CountDictTest(unittest.TestCase):
    def setUp(self) -> None:
        self.count_dict = CountDict()

    def test_something(self):
        cd = self.count_dict
        self.assertEqual(cd[2], 0, 'random access should be zero')
        self.assertEqual(cd['a'], 0, 'random access should be zero')
        cd[(1, 1)] += 2
        self.assertEqual(cd[(1, 1)], 2, 'contained values should be saved')
        key_list = list(cd.keys())
        self.assertTrue(1 not in key_list, 'unknown keys')
        self.assertTrue((1, 1) in key_list, 'known keys')
        cd[(1, 1)] -= 2
        key_list = list(cd.keys())
        self.assertTrue((1, 1) not in key_list, 'auto remove of keys')


class AutoAddCountDictTest(unittest.TestCase):
    def setUp(self) -> None:
        self.count_dict = AutoAddCountDict()

    def test_something(self):
        cd = self.count_dict
        self.assertTrue(type(cd[2]) == CountDict, 'random access should generate count_dict')
        cd[2][2] += 5
        self.assertEqual(cd[2][2], 5)


if __name__ == '__main__':
    unittest.main()
