from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

from datacheck import validate
from datacheck.core import List
from datacheck.exceptions import TypeValidationError, DataValidationError


class TestList(unittest.TestCase):
    def test_list_ok(self):
        input = [123, 456]
        result = validate(input, [int])
        self.assertIsNot(result, input, 'input list should not be modified')
        self.assertEqual(result, input, 'input should be copied into result')

    def test_list_less_than_or_equal_to_max_len(self):
        input = [123, 456]
        result = validate(input, List(int, max_len=2))
        self.assertIsNot(result, input, 'input list should not be modified')
        self.assertEqual(result, input, 'input should be copied into result')

    def test_list_too_long(self):
        expected_msg = r'<unnamed field>: List length must be less than 4, was 5'
        with self.assertRaisesRegexp(DataValidationError, expected_msg):
            validate([1, 2, 3, 4, 5], List(int, max_len=4))

    def test_list_type_error(self):
        expected_msg = r'<unnamed field>: Expected list, got int \(123\)'
        with self.assertRaisesRegexp(TypeValidationError, expected_msg):
            validate(123, [])

    def test_list_validation_error(self):
        expected_msg = r'<unnamed list>\[2\]: Expected int, got float \(0.9\)'
        with self.assertRaisesRegexp(TypeValidationError, expected_msg):
            validate([1, 1, 0.9, 1], [int])

    def test_list_of_list_ok(self):
        input = [[123, 456], []]
        result = validate(input, [[int]])
        self.assertIsNot(result, input, 'input list should not be modified')

        for i in range(3):
            self.assertIsNot(input[0], result[0],
                             'nested input list should not be modified')

        self.assertEqual(result, input, 'input should be copied into result')

    def test_list_of_list_validation_error(self):
        input = [[123, 456], [1, 0.8, 2]]
        expected_msg = r'<unnamed list>\[1\]\[1\]: Expected int, got float \(0.8\)'
        with self.assertRaisesRegexp(TypeValidationError, expected_msg):
            validate(input, [[int]])
