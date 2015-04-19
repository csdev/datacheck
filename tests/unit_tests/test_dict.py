from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

from mock import NonCallableMagicMock, patch, call

from datacheck.core import Dict, Required, Optional
from datacheck.exceptions import TypeValidationError, FieldValidationError


class TestDict(unittest.TestCase):
    def test_dict_ok(self):
        mock_validator = NonCallableMagicMock()
        dict_validator = Dict({
            'key1': mock_validator,
            'key2': mock_validator,
        })
        input_dict = {
            'key1': 'value1',
            'key2': 'value2'
        }

        # simulate underlying validator that passes all fields through
        # without validation errors
        def mock_validate(data, schema, **kwargs):
            return data

        with patch('datacheck.core._validate', side_effect=mock_validate) \
                as mock_validate:
            result = dict_validator.validate(input_dict)

        expected_calls = [
            call('value1', mock_validator, path=['key1']),
            call('value2', mock_validator, path=['key2']),
        ]
        mock_validate.assert_has_calls(expected_calls, any_order=True)

        self.assertIsNot(result, input_dict,
                         'input dict should not be modified')

        self.assertEqual(result, input_dict,
                         'input should be copied into result')

    def test_dict_type_error(self):
        mock_validator = NonCallableMagicMock()
        dict_validator = Dict({'mykey': mock_validator})
        input_dict = 123  # not a dict

        with self.assertRaises(TypeValidationError) as ctx:
            dict_validator.validate(input_dict, path=['mydict'])

        e = ctx.exception
        self.assertEqual(e.expected_type, dict)
        self.assertEqual(e.actual_type, int)
        self.assertEqual(e.actual_value, input_dict)
        self.assertEqual(e.path, ['mydict'])

    def test_dict_field_error(self):
        mock_validator = NonCallableMagicMock()
        dict_validator = Dict({
            'key1': mock_validator,
        })
        input_dict = {}

        with self.assertRaises(FieldValidationError) as ctx:
            dict_validator.validate(input_dict, path=['mydict'])

        e = ctx.exception
        self.assertEqual(e.expected_field, 'key1')
        self.assertEqual(e.path, ['mydict'])

    def test_dict_required_ok(self):
        mock_validator = NonCallableMagicMock()
        dict_validator = Dict({
            'key1': Required(mock_validator),
        })
        input_dict = {
            'key1': 'value1',
        }

        # simulate underlying validator that passes all fields through
        # without validation errors
        def mock_validate(data, schema, **kwargs):
            return data

        with patch('datacheck.core._validate', side_effect=mock_validate) \
                as mock_validate:
            result = dict_validator.validate(input_dict, path=['mydict'])

        self.assertIsNot(result, input_dict,
                         'input dict should not be modified')

        self.assertEqual(result, input_dict,
                         'input should be copied into result')

    def test_dict_required_error(self):
        mock_validator = NonCallableMagicMock()
        dict_validator = Dict({
            'key1': Required(mock_validator),
        })
        input_dict = {}

        with self.assertRaises(FieldValidationError) as ctx:
            dict_validator.validate(input_dict, path=['mydict'])

        e = ctx.exception
        self.assertEqual(e.expected_field, 'key1')
        self.assertEqual(e.path, ['mydict'])

    def test_dict_optional_ok(self):
        mock_validator = NonCallableMagicMock()
        dict_validator = Dict({
            'key1': Optional(mock_validator),
        })
        input_dict = {}

        result = dict_validator.validate(input_dict, path=['mydict'])

        self.assertIsNot(result, input_dict,
                         'input dict should not be modified')

        self.assertEqual(result, {})

    def test_dict_optional_default_ok(self):
        mock_validator = NonCallableMagicMock()
        dict_validator = Dict({
            'foo': Optional(mock_validator).default('bar'),
        })
        input_dict = {}

        result = dict_validator.validate(input_dict, path=['mydict'])

        self.assertIsNot(result, input_dict,
                         'input dict should not be modified')

        self.assertEqual(result, {'foo': 'bar'})
