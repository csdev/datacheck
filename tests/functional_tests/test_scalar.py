from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

from datacheck import validate
from datacheck.exceptions import TypeValidationError


class TestScalar(unittest.TestCase):
    def test_scalar_type_ok(self):
        y = validate(123, int)
        self.assertEqual(y, 123)

    def test_scalar_type_error(self):
        expected_msg = r'<unnamed field>: Expected int, got float \(0.123\)'
        with self.assertRaisesRegexp(TypeValidationError, expected_msg):
            validate(0.123, int)
