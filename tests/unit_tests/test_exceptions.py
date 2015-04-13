from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

from mock import patch

from datacheck.exceptions import TypeValidationError, FieldValidationError


class TestTypeValidationError(unittest.TestCase):
    def test_type_validation_error(self):
        e = TypeValidationError(None, int)
        self.assertEqual(e.expected_type, int)
        self.assertEqual(e.actual_type, type(None))
        self.assertEqual(e.actual_value, None)

        with patch('datacheck.exceptions.path_to_str', return_value='<PATH>'):
            self.assertEqual(str(e), '<PATH>: Expected int, got NoneType (None)')


class TestFieldValidationError(unittest.TestCase):
    def test_field_validation_error(self):
        e = FieldValidationError('foo')

        with patch('datacheck.exceptions.path_to_str', return_value='<PATH>'):
            self.assertEqual(str(e), '<PATH>: Missing required field "foo"')
