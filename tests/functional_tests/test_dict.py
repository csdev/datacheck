from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest

from datacheck import validate
from datacheck.exceptions import TypeValidationError


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
