from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

from datacheck.core import _get_validator, Validator, Type, List, Dict
from datacheck.exceptions import SchemaError


class TestGetValidator(unittest.TestCase):
    def test_get_validator_ok(self):
        schema = Validator()
        v = _get_validator(schema)
        self.assertIs(v, schema)

    def test_get_validator_type_ok(self):
        v = _get_validator(str)
        self.assertIsInstance(v, Type)
        self.assertEqual(v.expected_type, str)

    def test_get_validator_list_0_ok(self):
        v = _get_validator([])
        self.assertIsInstance(v, Type)
        self.assertEqual(v.expected_type, list)

    def test_get_validator_list_1_ok(self):
        list_item_schema = Validator()
        v = _get_validator([list_item_schema])
        self.assertIsInstance(v, List)
        self.assertEqual(v.schema, list_item_schema)

    def test_get_validator_list_error(self):
        with self.assertRaises(SchemaError):
            _get_validator([Validator(), Validator()])

    def test_get_validator_dict_ok(self):
        v = _get_validator({})
        self.assertIsInstance(v, Dict)
        self.assertEqual(v.schema, {})

    def test_get_validator_error(self):
        with self.assertRaises(SchemaError):
            _get_validator('not a validator')


class TestValidator(unittest.TestCase):
    def test_validator_not_implemented(self):
        v = Validator()
        with self.assertRaises(NotImplementedError):
            v.validate(None)
