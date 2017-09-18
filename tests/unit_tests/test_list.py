from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

from mock import NonCallableMagicMock, patch, call

from datacheck.core import List
from datacheck.exceptions import TypeValidationError, DataValidationError


class TestList(unittest.TestCase):
    def setUp(self):
        self.mock_validator = NonCallableMagicMock()

    def test_list_ok(self):
        list_validator = List(self.mock_validator)
        input_list = [1, 2, 3, 4]

        # simulate underlying validator that passes all list elements through
        # without validation errors
        def mock_validate(data, schema, **kwargs):
            return data

        with patch('datacheck.core._validate', side_effect=mock_validate) \
                as mock_validate:
            result = list_validator.validate(input_list, path=['mylist'])

        # underlying validator should be called for each element in the list
        mock_validate.assert_has_calls(
            [call(x, self.mock_validator, path=['mylist', i])
             for i, x in enumerate(input_list)])

        self.assertIsNot(result, input_list,
                         'input list should not be modified')

        self.assertEqual(result, input_list,
                         'input should be copied into result')

    def test_list_less_than_or_equal_to_max_len(self):
        list_validator = List(self.mock_validator, max_len=5)
        input_list = [1, 2, 3, 4, 5]

        def mock_validate(data, schema, **kwargs):
            return data

        with patch('datacheck.core._validate', side_effect=mock_validate) \
                as mock_validate:
            list_validator.validate(input_list, path=['mylist'])

    def test_list_too_long(self):
        list_validator = List(self.mock_validator, max_len=5)
        input_list = [1, 2, 3, 4, 5, 6]

        with self.assertRaises(DataValidationError):
            list_validator.validate(input_list, path=['mylist'])

    def test_list_type_error(self):
        list_validator = List(self.mock_validator)
        input_list = 123

        with self.assertRaises(TypeValidationError) as ctx:
            list_validator.validate(input_list, path=['mylist'])

        e = ctx.exception
        self.assertEqual(e.expected_type, list)
        self.assertEqual(e.actual_type, int)
        self.assertEqual(e.actual_value, input_list)
        self.assertEqual(e.path, ['mylist'])
