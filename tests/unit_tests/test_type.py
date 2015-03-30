from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

from datacheck.core import Type
from datacheck.exceptions import SchemaError, TypeValidationError


class TestType(unittest.TestCase):
    def test_type_ok(self):
        t = Type(int)
        self.assertEqual(t.expected_type, int)

        r = t.validate(12345, ['myint'])
        self.assertEqual(r, 12345)

    def test_type_init_error(self):
        with self.assertRaises(SchemaError):
            t = Type('foo')

    def test_type_validate_error(self):
        t = Type(int)
        self.assertEqual(t.expected_type, int)

        with self.assertRaises(TypeValidationError) as ctx:
            t.validate(0.123, ['myint'])

        e = ctx.exception
        self.assertEqual(e.expected_type, int)
        self.assertEqual(e.actual_type, float)
        self.assertEqual(e.actual_value, 0.123)
        self.assertEqual(e.path, ['myint'])
