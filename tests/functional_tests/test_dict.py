from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

from datacheck import validate, Required, Optional
from datacheck.exceptions import TypeValidationError, FieldValidationError


class TestDict(unittest.TestCase):
    def test_dict_ok(self):
        data = {
            'id': 120,
            'x': 15.0,
            'y': 10.4,
        }

        schema = {
            'id': int,
            'x': float,
            'y': float,
        }

        result = validate(data, schema)

        self.assertIsNot(result, data, 'input dict should not be modified')
        self.assertEqual(result, data, 'input should be copied into result')

    def test_dict_type_error(self):
        schema = {
            'id': int,
            'x': float,
            'y': float,
        }

        expected_msg = r'<unnamed field>: Expected dict, got int \(123\)'
        with self.assertRaisesRegexp(TypeValidationError, expected_msg):
            validate(123, schema)

    def test_dict_field_error(self):
        data = {
            # missing 'id'
            'x': 15.0,
            'y': 10.4,
        }

        schema = {
            'id': int,
            'x': float,
            'y': float,
        }

        expected_msg = r'<unnamed field>: Missing required field \"id\"'
        with self.assertRaisesRegexp(FieldValidationError, expected_msg):
            validate(data, schema)

    def test_dict_validation_error(self):
        data = {
            'id': -0.9999,  # not an int
            'x': 15.0,
            'y': 10.4,
        }

        schema = {
            'id': int,
            'x': float,
            'y': float,
        }

        expected_msg = r'id: Expected int, got float \(-0\.9999\)'
        with self.assertRaisesRegexp(TypeValidationError, expected_msg):
            validate(data, schema)

    def test_dict_field_spec_ok(self):
        data = {
            'id': 1234,
        }

        schema = {
            'id': Required(int),
            'name': Optional(str).default(None)
        }

        result = validate(data, schema)

        self.assertIsNot(result, data, 'input dict should not be modified')

        expected = {
            'id': 1234,
            'name': None,
        }
        self.assertEqual(result, expected)
