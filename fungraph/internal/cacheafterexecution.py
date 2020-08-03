from typing import Callable, Mapping, Any


class CacheAfterExecution():
    def __init__(self, f: Callable, cache: Mapping[str, Any], hash: str):
        self._cache = cache
        self._hash = hash
        self._f = f

    def __call__(self, *args, **kwargs) -> Any:
        value = self._f(*args, **kwargs)
        self._cache[self._hash] = value
        return value
