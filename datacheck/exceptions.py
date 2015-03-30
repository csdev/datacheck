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


class DataValidationError(ValidationError):
    def __init__(self):
        super(DataValidationError, self).__init__()
