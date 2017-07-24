# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys
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

    @unittest.skipUnless(sys.version_info.major == 2, 'python2 only')
    def test_py27_unicode_handling(self):
        e = TypeValidationError('À', int)
        with patch('datacheck.exceptions.path_to_str', return_value='<PATH>'):
            self.assertEqual(str(e), b'<PATH>: Expected int, got unicode (\xc3\x80)')


class TestFieldValidationError(unittest.TestCase):
    def test_field_validation_error(self):
        e = FieldValidationError('foo', path=['<PATH>'])

        with patch('datacheck.exceptions.path_to_str', return_value='<PATH>'):
            self.assertEqual(str(e), '<PATH>: Missing required field "foo"')

    def test_field_validation_error_no_path(self):
        e = FieldValidationError('foo')
        self.assertEqual(str(e), 'Missing required field "foo"')

    @unittest.skipUnless(sys.version_info.major == 2, 'python2 only')
    def test_py27_unicode_handling(self):
        e = FieldValidationError('À')
        self.assertEqual(str(e), b'Missing required field "\xc3\x80"')


class TestUnknownKeysError(unittest.TestCase):
    def test_unknown_keys_error(self):
        e = UnknownKeysError(['foo', 'bar', 123, None])

        with patch('datacheck.exceptions.path_to_str', return_value='<PATH>'):
            self.assertEqual(str(e), '<PATH>: Unknown keys: "foo", "bar", 123, None')

    @unittest.skipUnless(sys.version_info.major == 2, 'python2 only')
    def test_py27_unicode_handling(self):
        e = UnknownKeysError(['À'])

        with patch('datacheck.exceptions.path_to_str', return_value='<PATH>'):
            self.assertEqual(str(e), b'<PATH>: Unknown keys: "\xc3\x80"')


class TestDataValidationError(unittest.TestCase):
    def test_data_validation_error(self):
        e = DataValidationError('Name must start with a capital letter', 'asdf')

        with patch('datacheck.exceptions.path_to_str', return_value='<PATH>'):
            self.assertEqual(str(e), '<PATH>: Name must start with a capital letter (Received value: asdf)')

    @unittest.skipUnless(sys.version_info.major == 2, 'python2 only')
    def test_py27_unicode_handling(self):
        e = DataValidationError('Error', 'À')

        with patch('datacheck.exceptions.path_to_str', return_value='<PATH>'):
            self.assertEqual(str(e), b'<PATH>: Error (Received value: \xc3\x80)')
