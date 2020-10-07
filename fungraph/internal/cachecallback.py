from dask.callbacks import Callback

from fungraph.internal.dsktohash import dsktohash


class CacheCallback(Callback):
    def __init__(self, cache):
        super().__init__()
        self._cache = cache

    def _start(self, dsk):
        self._hashes = dsktohash(dsk)
        for key in dsk:
            if self._hashes[key] in self._cache:
                dsk[key] = (lambda k: self._cache[k], self._hashes[key])
        return

    def _posttask(self, key, value, dsk, state, id):
        self._cache[self._hashes[key]] = value
