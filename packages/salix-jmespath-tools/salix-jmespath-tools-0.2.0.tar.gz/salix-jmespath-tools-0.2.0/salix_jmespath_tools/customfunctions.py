
import re

from jmespath import functions, search


class CustomFunctions(functions.Functions):

    @functions.signature({'types': ['string']}, {'types': ['string']})
    def _func_re_search(self, s, pattern):
        return re.search(pattern, s) is not None

    @functions.signature({'types': ['object']})
    def _func_to_entries(self, o):
        """
        As per jq to_entries():

        {'a': 'A', 'b': 'B'} -> [{'key': 'a', 'value': 'A'}, {'key': 'b', 'value': 'B'}]

        """
        return [{'key': k, 'value': v} for k,v in o.items()]

    @functions.signature({'types': ['array']})
    def _func_from_entries(self, a):
        """
        As per jq from_entries():

        [{'key': 'a', 'value': 'A'}, {'key': 'b', 'value': 'B'}] -> {'a': 'A', 'b': 'B'}

        """
        return {item['key']: item['value'] for item in a}

    @functions.signature({'types': ['object']}, {'types': ['string']})
    def _func_with_entries(self, o, expr):
        """
        Similar to jq with_entries(), this applies expr as a filter combined with to_entries and from_entries:

            to_entries(@) | <filter> | from_entries(@)

        The filter expression must be such that it evaluates to either true or false.

        Example:

        > o = {"a": "A", "b": "B"}
        > with_entries(o, "key!=`b`")
        {"a": "A}

        """
        a = self._func_to_entries(o)
        a_map = [item for item in a if search(expr, item) is True]
        return self._func_from_entries(a_map)

    @functions.signature({'types': ['object']}, {'types': ['string', 'array']})
    def _func_remove_keys(self, o, keys):
        """
        Remove the keys listed in 'keys' array from the object. 

        Example:

        > o = {"a": "A", "b": "B", "c": "C"}
        > remove_keys(o, ['a', 'b'])
        {"c": "C"}

        keys can either be an array of keys, or a single key name supplied as a string
        e.g. remove_keys(@, 'a')

        """
        if isinstance(keys, str):
            keys = [keys]
        parts = [f'key!=`{k}`' for k in keys]
        expr = ' && '.join(parts)
        return self._func_with_entries(o, expr)

