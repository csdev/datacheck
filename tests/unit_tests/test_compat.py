from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys
import unittest

from datacheck.compat import (native_type,
                              int as _int, list as _list)


class TestNativeType(unittest.TestCase):
    def test_native_type(self):
        if sys.version_info[0] == 2:
            self.assertEqual(_int.__name__, 'newint')
            self.assertEqual(_list.__name__, 'newlist')

        self.assertEqual(native_type(_int).__name__, 'int')
        self.assertEqual(native_type(_list).__name__, 'list')
