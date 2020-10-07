from fungraph.cacheabc import Cache


class MemoryCache(Cache):
    def __init__(self):
        self._dict = dict()

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __contains__(self, __x: object) -> bool:
        return __x in self._dict

    def values(self):
        return self._dict.values()

    def keys(self):
        return self._dict.keys()

    def items(self):
        return self._dict.items()
