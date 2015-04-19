from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
from future.utils import iteritems

import inspect

from datacheck.compat import native_type
import datacheck.exceptions as exc
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
            raise exc.SchemaError()
    elif isinstance(schema, dict):
        return Dict(schema)

    raise exc.SchemaError()


def _validate(data, schema, **kwargs):
    v = _get_validator(schema)
    return v.validate(data, **kwargs)


class Validator(object):
    def validate(self, data, path=None, **kwargs):
        raise NotImplementedError()


class Type(Validator):
    def __init__(self, expected_type):
        if not inspect.isclass(expected_type):
            raise exc.SchemaError('expected_type must be a class type')

        self.expected_type = expected_type

    def validate(self, data, path=None, **kwargs):
        if not isinstance(data, self.expected_type):
            raise exc.TypeValidationError(data, self.expected_type, path=path)

        return data


class List(Validator):
    def __init__(self, schema):
        self.schema = schema

    def validate(self, data, path=None, **kwargs):
        if path is None:
            path = init_path()

        if not isinstance(data, list):
            raise exc.TypeValidationError(data, native_type(list), path=path)

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
    def __init__(self, schema):
        self.schema = schema

    def validate(self, data, path=None, **kwargs):
        if path is None:
            path = init_path()

        if not isinstance(data, dict):
            raise exc.TypeValidationError(data, native_type(dict), path=path)

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
                    raise exc.FieldValidationError(key, path=path)
            else:
                subpath = dict_item_path(path, key)
                output_dict[key] = _validate(actual_value, item_schema,
                                             path=subpath)

        # TODO: handling of unknown fields

        return output_dict
