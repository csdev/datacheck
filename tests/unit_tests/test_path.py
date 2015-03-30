from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

from datacheck.path import (init_path, dict_item_path, list_item_path,
                            _path_component_to_str, path_to_str)


class TestInitPath(unittest.TestCase):
    def test_init_path(self):
        self.assertEqual(init_path(), [])


class TestDictItemPath(unittest.TestCase):
    def test_dict_item_path(self):
        path = ['mydict']
        subpath = dict_item_path(path, 'key')
        self.assertEqual(path, ['mydict'])
        self.assertEqual(subpath, ['mydict', 'key'])


class TestListItemPath(unittest.TestCase):
    def test_list_item_path(self):
        path = ['mylist']
        subpath = list_item_path(path, 3)
        self.assertEqual(path, ['mylist'])
        self.assertEqual(subpath, ['mylist', 3])


class TestPathComponentToStr(unittest.TestCase):
    def test_path_component_to_str_should_handle_int(self):
        s = _path_component_to_str(1)
        self.assertEqual(s, '[1]')

    def test_path_component_to_str_should_handle_string(self):
        s = _path_component_to_str('foo')
        self.assertEqual(s, "['foo']")


class TestPathToStr(unittest.TestCase):
    def test_path_to_str_with_empty_path(self):
        s = path_to_str([])
        self.assertEqual(s, '<unnamed field>')

    def test_path_to_str(self):
        s = path_to_str(['mydict', 'mykey', 0])
        self.assertEqual(s, "mydict['mykey'][0]")

    def test_path_to_str_unnamed_list(self):
        s = path_to_str([4, 'mydict', 'mykey', 0])
        self.assertEqual(s, "<unnamed list>[4]['mydict']['mykey'][0]")
