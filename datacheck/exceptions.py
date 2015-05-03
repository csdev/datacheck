from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from datacheck.compat import native_data_type
from datacheck.path import path_to_str


class DatacheckException(Exception):
    pass


class SchemaError(DatacheckException):
    pass


class ValidationError(DatacheckException):
    def __init__(self, path=None):
        self.path = path


class MultipleValidationError(ValidationError):
    def __init__(self):
        pass


class TypeValidationError(ValidationError):
    def __init__(self, data, expected_type, path=None):
        super(TypeValidationError, self).__init__(path=path)
        self.expected_type = expected_type
        self.actual_type = native_data_type(data)
        self.actual_value = data

    def __str__(self):
        return '%s: Expected %s, got %s (%s)' % (
            path_to_str(self.path),
            self.expected_type.__name__,
            self.actual_type.__name__,
            self.actual_value,
        )


class FieldValidationError(ValidationError):
    def __init__(self, expected_field, path=None):
        super(FieldValidationError, self).__init__(path=path)
        self.expected_field = expected_field

    def __str__(self):
        msg = 'Missing required field "%s"' % self.expected_field
        if self.path:
            msg = path_to_str(self.path) + ': ' + msg
        return msg


class UnknownKeysError(ValidationError):
    def __init__(self, unknown_keys, path=None):
        super(UnknownKeysError, self).__init__(path=path)
        self.unknown_keys = unknown_keys

    def __str__(self):
        return '%s: Unknown keys: %s' % (
            path_to_str(self.path),
            ', '.join([('"%s"' % k if isinstance(k, str) else str(k))
                       for k in self.unknown_keys]),
        )


class DataValidationError(ValidationError):
    def __init__(self):
        super(DataValidationError, self).__init__()
