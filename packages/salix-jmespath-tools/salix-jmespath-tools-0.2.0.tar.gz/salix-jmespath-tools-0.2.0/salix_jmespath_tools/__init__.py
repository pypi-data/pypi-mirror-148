
__all__ = ['jp', 'CustomFunctions', 'JmesPathContainerMixin', 'JpDict', 'JpList', 'json_check', 'json_cast']


from functools import partial

import jmespath

from .customfunctions import *
from .jmespathtypes import *


# Define the jp convenience function
_options = jmespath.Options(custom_functions=CustomFunctions())
jp = partial(jmespath.search, options=_options)

