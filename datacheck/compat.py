from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from future.utils import native
from past.builtins import basestring as _basestring


# The future module redefines certain built-in types so that our python3
# code is also compatible with python2. However, we must be careful not to
# expose one of these redefined type objects to a python2 user who is not
# aware of the future module.
#
# http://python-future.org/what_else.html#passing-data-to-from-python-2-libraries
#
# Safe:
# type(2) --> int
#
# Unsafe; use this function to convert:
# int --> future.types.newint.newint
# type(int(2)) --> future.types.newint.newint
#
# On python3, this function is effectively a no-op.
#
def native_type(t):
    if t == int:  # future.types.newint.newint
        return native_data_type(0)
    elif t == list:  # future.types.newlist.newlist
        return native_data_type([])
    elif t == dict:  # future.types.newdict.newdict
        return native_data_type({})
    else:
        return t


def native_data_type(x):
    return type(native(x))


def is_unicode_or_byte_string(x):
    return isinstance(x, _basestring)
