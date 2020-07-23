import hashlib
from typing import Union, Mapping, Any

import cloudpickle
from dask.callbacks import Callback

from fungraph.internal.lockedcache import LockedCache

DEFAULT_CACHE_PATH = ".fungraphcache"


def cachecontext(cache: Union[str, Mapping[str, Any], None] = DEFAULT_CACHE_PATH) -> Callback:
    if cache is None:
        # null callback, does no caching
        return Callback()
    if isinstance(cache, str):
        cache = LockedCache(cache)
    return Cache(cache)


class Cache(Callback):

    def __init__(self, cache):
        super().__init__()
        self._cache = cache

    def _start(self, dsk):
        self._hashes = _dsktohash(dsk)
        for key in dsk:
            try:
                dsk[key] = self._cache[self._hashes[key]]
            except KeyError:
                pass
        return

    def _posttask(self, key, value, dsk, state, id):
        self._cache[self._hashes[key]] = value


def _dsktohash(dsk):
    return {k: hashlib.md5(cloudpickle.dumps(dsk[k])).hexdigest() for k in dsk.keys()}
