from typing import Union, Mapping, Any, Optional, Iterable

import dask
from dask.callbacks import Callback
from toolz import curry

from fungraph.internal.cachecallback import CacheCallback
from fungraph.internal.dsktohash import dsktohash
from fungraph.internal.lockedcache import LockedCache

DEFAULT_CACHE_PATH = ".fungraphcache"


def cachecontext(cache: Union[str, Mapping[str, Any], None] = DEFAULT_CACHE_PATH) -> Callback:
    """Enables automatic caching of function node results and values.

    Parameters
    ----------
    cache: Union[str, Mapping[str, Any], None]
        If `str` caches to the file system to a directory corresponding to this string. If the directory does not
        exist it is created.
        If Mapping[str, Any] is provided this object is used as the storage for the cache instead of the default filesystem
        method. For example, a standard dict would provide caching to memory.
        If `None`, no caching is enabled.

    Returns
    -------
    Callback
        a context manager that handles caching of function results and values.
    """
    if cache is None:
        # null callback, does no caching
        return Callback()
    if isinstance(cache, str):
        cache = LockedCache(cache)
    return dask.config.set(delayed_optimize=_optimize(cache=cache))


class CachedResult():
    def __init__(self, value):
        self._value = value

    def __call__(self, *args, **kwargs):
        return self._value

class CacheAfterExecution():
    def __init__(self, f, cache, hash):
        self._cache = cache
        self._hash = hash
        self._f = f

    def __call__(self, *args, **kwargs):
        print("calling:", self._f, args, kwargs)
        value = self._f(*args, **kwargs)
        self._cache[self._hash] = value
        return value

@curry
def _optimize(dsk: Mapping[str, Any], keys: Optional[Union[str, Iterable[str]]] = None,
              cache: Optional[Mapping[str, Any]] = None) -> Mapping[str, Any]:
    hashes = dsktohash(dsk)
    result = {}
    for key in dsk:
        try:
            result[key] = cache[hashes[key]] #(CachedResult(cache[hashes[key]]), )
        except KeyError:
            c = dsk[key]
            if dask.istask(c):
                result[key] = (CacheAfterExecution(c[0], cache, hashes[key]),) + c[1:]
            else:
                result[key] = dsk[key]
    return result
