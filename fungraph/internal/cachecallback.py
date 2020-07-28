import hashlib
from typing import Mapping, Tuple, Any

import cloudpickle
from dask.callbacks import Callback


class CacheCallback(Callback):

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
