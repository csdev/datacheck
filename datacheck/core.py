from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
from future.utils import iteritems

import inspect

from datacheck.compat import native_type
from datacheck.exceptions import (SchemaError, TypeValidationError,
                                  FieldValidationError, UnknownKeysError,
                                  DataValidationError)
from datacheck.path import init_path, list_item_path, dict_item_path


def validate(data, schema, **kwargs):
    if 'path' not in kwargs:
        kwargs['path'] = init_path()
    return _validate(data, schema, **kwargs)


def _get_validator(schema):
    if isinstance(schema, Validator):
        return schema
    elif inspect.isclass(schema):
        return Type(schema)
    elif isinstance(schema, list):
        l = len(schema)
        if l == 0:
            return Type(native_type(list))
        elif l == 1:
            return List(schema[0])
        else:
            raise SchemaError()
    elif isinstance(schema, dict):
        return Dict(schema)

    raise SchemaError()


def _validate(data, schema, **kwargs):
    v = _get_validator(schema)
    return v.validate(data, **kwargs)


class Validator(object):
    def validate(self, data, path=None):
        raise NotImplementedError()


class Type(Validator):
    def __init__(self, expected_type):
        if not inspect.isclass(expected_type):
            raise SchemaError('expected_type must be a class type')

        self.expected_type = expected_type

    def validate(self, data, path=None):
        if not isinstance(data, self.expected_type):
            raise TypeValidationError(data, self.expected_type, path=path)

        return data


class List(Validator):
    def __init__(self, schema, max_len=None):
        self.schema = schema
        self.max_len = max_len

    def validate(self, data, path=None):
        if path is None:
            path = init_path()

        if not isinstance(data, list):
            raise TypeValidationError(data, native_type(list), path=path)

        len_data = len(data)
        if self.max_len is not None and len_data > self.max_len:
            error_msg = ('List length must be '
                         'less than %s, was %s' % (self.max_len, len_data))
            raise DataValidationError(error_msg, data, path=path)

        output_list = []

        for i, x in enumerate(data):
            subpath = list_item_path(path, i)
            output_list.append(_validate(x, self.schema, path=subpath))

        return output_list


class DictField(object):
    def __init__(self, schema):
        self.schema = schema


class Required(DictField):
    pass


class Optional(DictField):
    def __init__(self, schema):
        super(Optional, self).__init__(schema)
        self.has_default = False
        self.default_value = None

    def default(self, x):
        self.has_default = True
        self.default_value = x
        return self


class Dict(Validator):
    def __init__(self, schema, allow_unknown=False):
        self.schema = schema
        self.allow_unknown = allow_unknown

    def validate(self, data, path=None):
        if path is None:
            path = init_path()

        if not isinstance(data, dict):
            raise TypeValidationError(data, native_type(dict), path=path)

        unknown_keys = set(data)
        output_dict = {}

        for key, field_spec in iteritems(self.schema):
            if isinstance(field_spec, DictField):
                item_schema = field_spec.schema
                is_optional = isinstance(field_spec, Optional)
            else:
                item_schema = field_spec
                is_optional = False

            try:
                actual_value = data[key]
            except KeyError:
                if is_optional:
                    if field_spec.has_default:
                        output_dict[key] = field_spec.default_value
                else:
                    raise FieldValidationError(key, path=path)
            else:
                unknown_keys.remove(key)
                subpath = dict_item_path(path, key)
                output_dict[key] = _validate(actual_value, item_schema,
                                             path=subpath)

        if (not self.allow_unknown) and unknown_keys:
            raise UnknownKeysError(unknown_keys, path=path)
        else:
            output_dict.update({k: data[k] for k in unknown_keys})

        return output_dict
