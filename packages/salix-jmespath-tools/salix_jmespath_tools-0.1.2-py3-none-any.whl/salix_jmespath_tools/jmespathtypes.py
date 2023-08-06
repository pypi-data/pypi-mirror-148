

__all__ = ['JmesPathContainerMixin', 'JpDict', 'JpList', 'json_check', 'json_cast']


import json
from functools import partial

import jmespath

from .customfunctions import CustomFunctions


_options = jmespath.Options(custom_functions=CustomFunctions())
_jpr = partial(jmespath.search, options=_options)


def json_check(obj):
    try:
        json.loads(json.dumps(obj))
    except TypeError:
        return False
    return True


def json_cast(obj):
    return json.loads(json.dumps(obj))


class JmesPathContainerMixin():

    def jp(self, expr):
        return _jpr(expr, json_cast(self))


class JpDict(JmesPathContainerMixin, dict):
    pass


class JpList(JmesPathContainerMixin, dict):
    pass
