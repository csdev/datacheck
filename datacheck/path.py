from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from datacheck.compat import is_unicode_or_byte_string


def init_path():
    return []


def dict_item_path(path, field_name):
    return path + [field_name]


def list_item_path(path, list_index):
    return path + [list_index]


def _path_component_to_str(path_component):
    if isinstance(path_component, int):
        return '[%d]' % path_component
    elif is_unicode_or_byte_string(path_component):
        return "['%s']" % path_component
    else:
        raise ValueError('invalid path_component')


def path_to_str(path):
    if not path:
        return '<unnamed field>'

    base = ''
    subpath_idx = 0
    if isinstance(path[0], int):
        base = '<unnamed list>'
    elif is_unicode_or_byte_string(path[0]):
        base = path[0]
        subpath_idx = 1

    return base + ''.join([_path_component_to_str(pc)
                           for pc in path[subpath_idx:]])
