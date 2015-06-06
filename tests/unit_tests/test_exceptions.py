from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

from mock import patch

from datacheck.exceptions import (TypeValidationError, FieldValidationError,
                                  UnknownKeysError, DataValidationError)


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
        e = FieldValidationError('foo', path=['<PATH>'])

        with patch('datacheck.exceptions.path_to_str', return_value='<PATH>'):
            self.assertEqual(str(e), '<PATH>: Missing required field "foo"')

    def test_field_validation_error_no_path(self):
        e = FieldValidationError('foo')
        self.assertEqual(str(e), 'Missing required field "foo"')


class TestUnknownKeysError(unittest.TestCase):
    def test_unknown_keys_error(self):
        e = UnknownKeysError(['foo', 'bar', 123, None])

        with patch('datacheck.exceptions.path_to_str', return_value='<PATH>'):
            self.assertEqual(str(e), '<PATH>: Unknown keys: "foo", "bar", 123, None')


class TestDataValidationError(unittest.TestCase):
    def test_data_validation_error(self):
        e = DataValidationError('Name must start with a capital letter', 'asdf')

        with patch('datacheck.exceptions.path_to_str', return_value='<PATH>'):
            self.assertEqual(str(e), '<PATH>: Name must start with a capital letter (Received value: asdf)')
