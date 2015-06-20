import sys
import unittest

from datacheck.path import path_to_str


@unittest.skipUnless(sys.version_info.major == 2,
                     'This test is only valid for python2')
class TestPathToStr(unittest.TestCase):
    def test_path_to_str(self):
        path = ['foo', 'bar', 'baz']
        for path_item in path:
            self.assertNotIsInstance(path_item, unicode)

        s = path_to_str(path)
        self.assertEqual(s, "foo['bar']['baz']")
