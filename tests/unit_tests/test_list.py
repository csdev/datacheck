from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

from mock import NonCallableMagicMock, patch, call

from datacheck.core import List
from datacheck.exceptions import TypeValidationError


class TestList(unittest.TestCase):
    def test_list_ok(self):
        mock_validator = NonCallableMagicMock()
        list_validator = List(mock_validator)
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
            [call(x, mock_validator, path=['mylist', i])
             for i, x in enumerate(input_list)])

        self.assertIsNot(result, input_list,
                         'input list should not be modified')

        self.assertEqual(result, input_list,
                         'input should be copied into result')

    def test_list_type_error(self):
        mock_validator = NonCallableMagicMock()
        list_validator = List(mock_validator)
        input_list = 123

        with self.assertRaises(TypeValidationError) as ctx:
            list_validator.validate(input_list, path=['mylist'])

        e = ctx.exception
        self.assertEqual(e.expected_type, list)
        self.assertEqual(e.actual_type, int)
        self.assertEqual(e.actual_value, input_list)
        self.assertEqual(e.path, ['mylist'])
